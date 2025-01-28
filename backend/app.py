from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import joblib
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# โหลดโมเดลและ Vectorizer จากไฟล์ที่เพิ่งสร้าง
vectorizer = joblib.load("backend/model/vectorizer.pkl")
model = joblib.load("backend/model/model.pkl")

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
        except Exception as e:
            raise HTTPException(status_code=400, detail="Cannot fetch article from the URL provided.")
        text_to_check = article_text
    elif request.text:
        text_to_check = request.text
    else:
        raise HTTPException(status_code=400, detail="No text or URL provided.")

    # แปลงข้อความด้วย Vectorizer ที่โหลดมา
    X_vec = vectorizer.transform([text_to_check])
    # ทำนายโอกาสที่เป็นข่าวจริง (หรือปลอม)
    # สมมติ label: real=0, fake=1 => predict_proba[:, 1] คือโอกาสเป็น fake
    prob_fake = model.predict_proba(X_vec)[0][1]
    # ถ้าอยากแสดง score ความน่าเชื่อถือในมุมกลับกัน (เช่น score=โอกาสเป็นจริง)
    # อาจจะใช้ score = (1 - prob_fake)*100 เพื่อเป็นเปอร์เซ็นต์ความน่าเชื่อถือ

    score_real = (1 - prob_fake) * 100
    explanation = "The score represents the model's confidence that the news is real."
    recommendations = [
        {"title": "BBC News", "url": "https://www.bbc.com"},
        {"title": "Reuters", "url": "https://www.reuters.com"}
    ]

    return {
        "score": score_real,
        "explanation": explanation,
        "recommendations": recommendations
    }


def fetch_article_text(url: str) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = " ".join([p.get_text() for p in paragraphs])
    return article_text


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
