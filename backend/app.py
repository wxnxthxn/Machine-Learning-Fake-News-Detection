from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)

# กำหนด MODEL_NAME และ MODEL_PATH สำหรับ ThaiBERT
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
MODEL_PATH = "backend/model/model.pth"  # ปรับ path ให้ตรงกับโครงสร้างโปรเจกต์

# โหลด Tokenizer และ Model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

app = FastAPI()

# ตั้งค่า CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model สำหรับรับ Request ผ่าน API
class CheckRequest(BaseModel):
    text: str  # ตอนนี้เราใช้แค่ข้อความที่ไฮไลท์ (text) เท่านั้น

@app.post("/check")
def check_fakenews(request: CheckRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided.")

    text_to_check = request.text

    # ใช้โมเดล ThaiBERT วิเคราะห์ข่าวจากข้อความที่ไฮไลท์
    inputs = tokenizer(text_to_check, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    ai_score = (1 - torch.softmax(logits, dim=1)[0][1].item()) * 100

    # ส่งผลลัพธ์กลับ
    return {
        "source": "ThaiBERT",
        "ai_score": ai_score
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
