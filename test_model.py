import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import joblib
import os

# 1. ตรวจสอบและสร้างโฟลเดอร์ 'model' หากยังไม่มี
output_dir = 'model'
os.makedirs(output_dir, exist_ok=True)

# 2. โหลด Dataset
df = pd.read_csv('news_data.csv')  # เปลี่ยนตาม path ของไฟล์จริง

# 3. แมป Label ให้เป็นตัวเลข (0=real, 1=fake)
df['label'] = df['label'].map({'Real': 0, 'Fake': 1})

# 3.1 ลบแถวใด ๆ ที่ label เป็น NaN (กรณีบางแถวไม่ใช่ 'real' หรือ 'fake')
df = df.dropna(subset=['label'])

# 3.2 ตรวจสอบ / จัดการ NaN ในคอลัมน์ 'description'
df['description'] = df['description'].fillna('')  # แทน NaN ด้วยสตริงว่าง

# 4. แบ่งชุดข้อมูลเป็น Training / Testing
X = df['description']  # ข้อความข่าว
y = df['label']        # ประเภทข่าว (0/1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. แปลงข้อความเป็นเวกเตอร์ TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)  # ใช้คำ 5000 คำที่พบบ่อยที่สุด
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 6. สร้างและฝึก Logistic Regression Model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 7. บันทึกโมเดลและ Vectorizer
joblib.dump(model, os.path.join(output_dir, 'model.pkl'))
joblib.dump(vectorizer, os.path.join(output_dir, 'vectorizer.pkl'))
print("Model and Vectorizer saved successfully!")

# 8. ทำนายผลลัพธ์
y_pred = model.predict(X_test_tfidf)

# 9. ประเมินผลโมเดล
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 10. Cross-Validation (ประเมินความเสถียรด้วย CV=5)
scores = cross_val_score(model, vectorizer.transform(X), y, cv=5)
print("Cross-Validation Accuracy:", scores.mean())

# 11. ทดสอบข้อความตัวอย่าง
sample_texts = [
    # *** เน้นรูปแบบที่คล้าย "ข่าวปลอม" ใน dataset ***
    "ปปง. เปิดให้ผู้เสียหายแจ้งขอคืนเงินจากแก๊งคอลเซ็นเตอร์ผ่านเพจ Crime Suppression Division",
    "ธนาคารอิสลามแห่งประเทศไทย เปิดสินเชื่อวงเงิน 3 แสนบาท ไม่ต้องมีคนค้ำ",
    "ตลาดหลักทรัพย์ฯ เปิดสอนเล่นหุ้น เริ่มต้นเพียง 1,000 บาท ลงทะเบียนทางเพจปลอม",
    "กรุงไทยเปิดให้ลงทุน 1,200 บาท ได้ผลตอบแทน 30% ภายในสัปดาห์เดียว",

    # *** เน้นรูปแบบที่น่าจะเป็น "ข่าวจริง" หรือทั่วไป ***
    "รัฐบาลประกาศแผนพัฒนาระบบ EEC-D ขับเคลื่อนเขตเศรษฐกิจตะวันออกด้วยดิจิทัล",
    "ผู้เสียหายเตือนภัยแก๊งคอลเซ็นเตอร์ผ่านสื่อมวลชน เพื่อไม่ให้ใครหลงเชื่อ",
    "ตลาดหลักทรัพย์ฯ รายงานผลประกอบการไตรมาสที่ 2 ของปี 2024",
    "สำนักข่าวไทยเผยแพร่ข้อมูลการลงทุนที่ได้รับการกำกับดูแลโดย ก.ล.ต. อย่างถูกต้อง"
]

sample_tfidf = vectorizer.transform(sample_texts)
sample_predictions = model.predict(sample_tfidf)

print("\n--- News Sample Test Results ---")
for text, pred in zip(sample_texts, sample_predictions):
    label_str = "Fake" if pred == 1 else "Real"
    print(f"'{text}' => {label_str}")
