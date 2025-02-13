import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# ✅ ตั้งค่า Path ที่สัมพันธ์กับตำแหน่งของ script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../../dataset/clean_news_data.csv")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "../../backend/model/model_latest.pth")

# ✅ โหลด Dataset ข่าวที่ทำความสะอาดแล้ว
df = pd.read_csv(DATASET_PATH, encoding="utf-8")

# ✅ ตรวจสอบว่ามีคอลัมน์ที่ใช้เทรนหรือไม่
if "text" in df.columns:
    text_column = "text"
elif "description" in df.columns:
    text_column = "description"
else:
    raise ValueError("❌ ไม่มีคอลัมน์ข้อความที่ใช้เทรน (text หรือ description)")

# ✅ แปลง Label เป็นตัวเลข (0/1)
df["label"] = LabelEncoder().fit_transform(df["label"])

# ✅ ลบค่าที่เป็น NaN
df = df.dropna().reset_index(drop=True)

# ✅ แบ่งข้อมูล train/test (ใช้ stratify เพื่อรักษาสัดส่วน)
X_train, X_test, y_train, y_test = train_test_split(
    df[text_column], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# ✅ โหลด ThaiBERT Tokenizer
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ✅ ตั้งค่าการ Tokenize
MAX_LENGTH = 256
X_train_tokens = tokenizer(list(X_train), padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
X_test_tokens = tokenizer(list(X_test), padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")

# ✅ รีเซ็ต Index และแปลงค่าเป็น Tensor
y_train = torch.tensor(y_train.values, dtype=torch.long)
y_test = torch.tensor(y_test.values, dtype=torch.long)

# ✅ ใช้ DataLoader เพื่อลดการใช้ RAM
BATCH_SIZE = 8
train_dataset = TensorDataset(X_train_tokens["input_ids"], X_train_tokens["attention_mask"], y_train)
test_dataset = TensorDataset(X_test_tokens["input_ids"], X_test_tokens["attention_mask"], y_test)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# ✅ โหลดโมเดล ThaiBERT
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2).to(device)

# ✅ เทรนโมเดล
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
EPOCHS = 5

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for batch in train_loader:
        input_ids, attention_mask, labels = [x.to(device) for x in batch]
        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"✅ Epoch {epoch + 1}/{EPOCHS}, Loss: {total_loss:.4f}")

# ✅ บันทึกโมเดลใหม่
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"✅ Model retrained successfully! Saved at {MODEL_SAVE_PATH}")
