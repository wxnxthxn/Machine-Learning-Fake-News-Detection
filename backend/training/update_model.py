import shutil
import os
import torch
from transformers import AutoModelForSequenceClassification

# ✅ กำหนด path โดยอ้างอิงตำแหน่งของไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ตำแหน่งไฟล์ update_model.py
MODEL_DIR = os.path.join(BASE_DIR, "../model")

LATEST_MODEL = os.path.join(MODEL_DIR, "model_latest.pth")
CURRENT_MODEL = os.path.join(MODEL_DIR, "model.pth")
MODEL_UPDATE_FLAG = os.path.join(MODEL_DIR, "updated.flag")

def is_new_model_better():
    """
    ตรวจสอบว่าโมเดลใหม่ดีกว่าโมเดลเก่าหรือไม่
    """
    if not os.path.exists(CURRENT_MODEL):  # ถ้าไม่มีโมเดลเก่า ให้ถือว่าอัปเดตได้เลย
        return True

    try:
        latest_model = torch.load(LATEST_MODEL, map_location=torch.device("cpu"))
        current_model = torch.load(CURRENT_MODEL, map_location=torch.device("cpu"))

        # เปรียบเทียบโมเดลใหม่กับโมเดลเก่า
        if latest_model != current_model:
            return True
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        return True  # ถ้าโหลดโมเดลเก่าไม่ได้ ให้ถือว่าโมเดลใหม่ต้องใช้แทน

    return False

try:
    if os.path.exists(LATEST_MODEL) and is_new_model_better():
        shutil.copy(LATEST_MODEL, CURRENT_MODEL)
        with open(MODEL_UPDATE_FLAG, "w") as f:
            f.write("updated")
        print("✅ Model updated successfully!")
    else:
        print("⚠️ No update needed, model is already the best version.")
except Exception as e:
    print(f"⚠️ Model update failed: {e}")
