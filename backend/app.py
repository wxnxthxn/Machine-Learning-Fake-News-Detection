from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import joblib
import requests
from bs4 import BeautifulSoup
import os
from google.oauth2 import service_account
import googleapiclient.discovery

# ✅ ตั้งค่า API Key สำหรับ Google Fact Check API
GOOGLE_API_KEY = "AIzaSyDVVcqu_hUsnMKuvKHDR6s__ebXbMZ7pK0"

# ✅ โหลดโมเดล AI (DistilBERT + LSTM)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")
model_path = os.path.join(BASE_DIR, "model", "model.pkl")

vectorizer = joblib.load(vectorizer_path)
model = joblib.load(model_path)

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
    if request.url:
        try:
            article_text = fetch_article_text(request.url)
        except Exception:
            raise HTTPException(status_code=400, detail="Cannot fetch article from the URL provided.")
        text_to_check = article_text
    elif request.text:
        text_to_check = request.text
    else:
        raise HTTPException(status_code=400, detail="No text or URL provided.")

    # ✅ 1. ลองเช็คกับ AFP Fact Check ก่อน
    afp_result = afp_fact_check(text_to_check)
    if afp_result:
        return {
            "source": "AFP Fact Check",
            "result": afp_result
        }

    # ✅ 2. ใช้ AI (DistilBERT + LSTM) วิเคราะห์
    X_vec = vectorizer.transform([text_to_check])
    prob_fake = model.predict_proba(X_vec)[0][1]
    score_real = (1 - prob_fake) * 100

    # ✅ 3. ถ้า AI ไม่แน่ใจ (40%-60%) → ใช้ Google API
    if 40 <= score_real <= 60:
        google_result = google_fact_check(text_to_check)
        if google_result:
            return {
                "source": "Google Fact Check",
                "result": google_result
            }

    return {
        "source": "AI Model",
        "score": score_real
    }

# ✅ ฟังก์ชันดึงข่าวจาก AFP Fact Check Thailand
def afp_fact_check(query: str):
    url = "https://factcheckthailand.afp.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            title = article.find('h2').text if article.find('h2') else "No title"
            link = article.find('a')['href'] if article.find('a') else "No link"
            if query in title:
                return {"title": title, "url": link}
    return None

# ✅ ใช้ Google Fact Check API เพื่อตรวจสอบข่าว
def google_fact_check(query: str):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
