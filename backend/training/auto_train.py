import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# ✅ Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../../dataset/clean_news_data.csv")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "../../backend/model/model_latest.pth")

# ✅ Load Dataset
df = pd.read_csv(DATASET_PATH, encoding="utf-8")

# ✅ Check text column
if "text" in df.columns:
    text_column = "text"
elif "description" in df.columns:
    text_column = "description"
else:
    raise ValueError("❌ ไม่มีคอลัมน์ข้อความที่ใช้เทรน (text หรือ description)")

# ✅ Drop NaN and encode labels
df = df.dropna(subset=[text_column, 'label']).reset_index(drop=True)
df["label"] = LabelEncoder().fit_transform(df["label"])

if df.empty:
    raise ValueError("❌ Dataframe is empty after cleaning.")

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df[text_column],
    df["label"],
    test_size=0.2,
    stratify=df["label"],
    random_state=42
)

# ✅ Load Tokenizer
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ✅ Tokenize dataset
MAX_LENGTH = 256
train_tokens = tokenizer(list(X_train), padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
test_tokens = tokenizer(list(X_test), padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")

# ✅ Convert labels to tensor
y_train = torch.tensor(y_train.values)
y_test = torch.tensor(y_test.values)

# ✅ DataLoader
BATCH_SIZE = 8
train_dataset = TensorDataset(
    train_tokens["input_ids"],
    train_tokens["attention_mask"],
    y_train
)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# ✅ Model preparation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2).to(device)

# ✅ Training setup
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
EPOCHS = 5

# ✅ Train loop
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for input_ids, attention_mask, labels in DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True):
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    print(f"✅ Epoch {epoch + 1}/{EPOCHS}, Loss: {avg_loss:.4f}")

# ✅ Save model
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"✅ Model retrained successfully! Saved at {MODEL_SAVE_PATH}")
