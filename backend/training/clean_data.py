import pandas as pd
import os

# ✅ ใช้ path ที่สัมพันธ์กับตำแหน่งของไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path ของ training/
DATASET_PATH = os.path.join(BASE_DIR, "../../dataset/news_data.csv")  # ✅ Path ที่ถูกต้อง!

def clean_data(csv_path: str) -> pd.DataFrame:
    """
    ทำความสะอาดชุดข้อมูล:
    1) แปลงค่า 'label' เป็นตัวเลข (real=0, fake=1)
    2) ลบข้อมูลที่ไม่ใช่ real/fake
    3) แก้ไขค่าว่างใน 'description'
    """
    df = pd.read_csv(csv_path)
    df['label'] = df['label'].astype(str).str.lower().map({'real': 0, 'fake': 1})
    df = df.dropna(subset=['label'])
    df['description'] = df['description'].fillna('')
    return df

if __name__ == "__main__":
    cleaned_df = clean_data(DATASET_PATH)  # ✅ ใช้ตัวแปร DATASET_PATH
    cleaned_df.to_csv(os.path.join(BASE_DIR, "../../dataset/clean_news_data.csv"), index=False)  # ✅ บันทึกไฟล์ไปที่ dataset/
    print("✅ Data cleaned and saved!")
