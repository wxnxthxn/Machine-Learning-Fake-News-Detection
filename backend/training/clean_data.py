import pandas as pd
import os

# ✅ ใช้ path ที่สัมพันธ์กับตำแหน่งของไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path ของ training/
DATASET_PATH = os.path.join(BASE_DIR, "../../dataset/news_data.csv")  # ✅ Path ที่ถูกต้อง!

def clean_data(csv_path: str) -> pd.DataFrame:
    """
    ทำความสะอาดชุดข้อมูล:
    1) แปลงค่า 'label' เป็นตัวเลข (real=0, fake=1) สำหรับข่าวที่มี label นี้
    2) เติมค่า NaN ใน 'label' ด้วย "Unknown" แทนการลบ
    3) แก้ไขค่าว่างใน 'description'
    """
    df = pd.read_csv(csv_path)
    # เติมค่า NaN ในคอลัมน์ 'label' ด้วย "Unknown"
    df['label'] = df['label'].fillna("Unknown")
    # แปลง label เฉพาะสำหรับข่าวที่มี label 'real' หรือ 'fake'
    def map_label(x):
        if isinstance(x, str):
            x_lower = x.lower()
            if x_lower == 'real':
                return 0
            elif x_lower == 'fake':
                return 1
        return x  # สำหรับ "Unknown" หรือค่าที่ไม่ตรงกัน จะเก็บไว้เดิม
    df['label'] = df['label'].apply(map_label)
    # แก้ไขค่าว่างใน 'description'
    df['description'] = df['description'].fillna('')

    return df

if __name__ == "__main__":
    cleaned_df = clean_data(DATASET_PATH)  # ✅ ใช้ตัวแปร DATASET_PATH
    cleaned_df.to_csv(os.path.join(BASE_DIR, "../../dataset/clean_news_data.csv"), index=False)  # ✅ บันทึกไฟล์ไปที่ dataset/
    print("✅ Data cleaned and saved!")
