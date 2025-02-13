from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ✅ ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)

# ✅ โหลด ThaiBERT (WangchanBERTa)
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
MODEL_PATH = "backend/model/model.pth"  # ✅ เปลี่ยน path ตามโครงสร้างโปรเจกต์ใหม่

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

# ✅ ตั้งค่า Google Fact Check API Key
GOOGLE_API_KEY = "AIzaSyDVVcqu_hUsnMKuvKHDR6s__ebXbMZ7pK0"

app = FastAPI()

# ✅ ตั้งค่า CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CheckRequest(BaseModel):
    text: str = None
    url: str = None

@app.post("/check")
def check_fakenews(request: CheckRequest):
    if request.text:
        text_to_check = request.text
    elif request.url:
        text_to_check = fetch_article_text(request.url)
    else:
        raise HTTPException(status_code=400, detail="No text or URL provided.")

    # ✅ 1. ใช้ AI ThaiBERT วิเคราะห์ข่าว
    inputs = tokenizer(text_to_check, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    ai_score = (1 - torch.softmax(logits, dim=1)[0][1].item()) * 100

    # ✅ 2. ถ้า AI ไม่มั่นใจ (40% - 60%) → ใช้ Google Fact Check API
    google_result = None
    if 40 <= ai_score <= 60:
        google_result = google_fact_check(text_to_check)
        if not google_result:
            google_result = {"message": "❌ ไม่พบข้อมูลจาก Google Fact Check"}

    return {
        "source": "Hybrid (ThaiBERT + Google Fact Check)",
        "ai_score": ai_score,
        "google_fact_check": google_result
    }

# ✅ ฟังก์ชันดึงข่าวจาก Google Fact Check API
def google_fact_check(query: str):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning("⚠️ Google Fact Check API ไม่สามารถดึงข้อมูลได้")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"🔴 ไม่สามารถเชื่อมต่อ Google API: {str(e)}")
        return None

# ✅ ฟังก์ชันดึงเนื้อหาข่าวจาก URL
def fetch_article_text(url: str) -> str:
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs]) if paragraphs else "No content found."
    except Exception:
        return "Unable to fetch content."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  # ✅ เปลี่ยนเป็นพอร์ต 8000
