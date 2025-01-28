import pandas as pd

def clean_data(csv_path: str) -> pd.DataFrame:
    """
    อ่านไฟล์ CSV ที่มีคอลัมน์ 'label' และ 'description'
    1) แปลงค่า 'label' เป็นตัวพิมพ์เล็ก
    2) map 'real' -> 0, 'fake' -> 1
    3) ตัดแถวที่ค่า label เป็น NaN (เพราะ map แล้วไม่ได้)
    4) fillna ใน 'description' ด้วยสตริงว่าง
    5) return DataFrame ที่สะอาด
    """

    # 1. อ่านไฟล์ CSV
    df = pd.read_csv(csv_path)
    print(f"[INFO] Initial shape: {df.shape}")

    # 2. แปลง label เป็นตัวพิมพ์เล็ก (ป้องกัน 'Real' 'Fake' ตัวพิมพ์ใหญ่ไม่ match)
    df['label'] = df['label'].astype(str).str.lower()  # หากเดิมเป็น NaN อาจกลายเป็น 'nan'

    # 3. map ค่า
    print("[INFO] Unique labels (before map):", df['label'].unique())
    df['label'] = df['label'].map({'real': 0, 'fake': 1})

    # 4. ตัดแถวที่ label เป็น NaN (เกิดจากค่าไม่ใช่ real/fake)
    df = df.dropna(subset=['label'])
    print("[INFO] Shape after drop rows with invalid label:", df.shape)

    # 5. fillna คอลัมน์ description ด้วยสตริงว่าง
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    else:
        # ถ้าไม่มีคอลัมน์ description อาจขึ้นเตือน หรือหยุด
        print("[WARNING] No 'description' column found in CSV!")

    # ตรวจสอบผล
    print("[INFO] Unique labels (after map & dropna):", df['label'].unique())
    print("[INFO] Final shape:", df.shape)

    return df

if __name__ == "__main__":
    # ทดสอบการใช้งาน
    cleaned_df = clean_data("news_data.csv")
    # จากนั้น cleaned_df พร้อมนำไปแบ่ง train/test, vectorizer ฯลฯ
