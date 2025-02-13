### `📰 Machine Learning Fake News Detection`

 ## 🔍 **Project Overview**
This project provides a **Chrome Extension** and a **FastAPI** backend to detect fake news based on text or article URLs. It uses a trained **ThaiBERT (WangchanBERTa) model** to classify news as *real* or *fake*. The system can also give a trust score and explanations.

## 📌Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Chrome Extension](#chrome-extension)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## 📌Features

✅ Classifies news articles as **Real or Fake**  
✅ **Trained ThaiBERT (WangchanBERTa) model** for predictions  
✅ Supports **both direct text input analysis**  
✅ Provides a **FastAPI-based REST API** for integration into other systems  
✅ Offers **trusted news recommendations** if an article is likely fake  

---
## 🛠 **Tech Stack**
- **Programming Language:** Python
- **Framework:** FastAPI
- **Machine Learning Model:** ThaiBERT (WangchanBERTa) for text classification
- **Data Processing:** Pandas, PyTorch, Transformers
- **Storage & Deployment:** GitHub, Model Persistence
---
## Architecture

```bash
ProjectMLFakeNewsCheck/
├─ backend/
│   ├─ app.py
│   ├─ model/
│   │   ├─ model_latest.pth
│   │   ├─ update_model.py
│   │   └─ predict.py
│   ├─ training/
│   │   ├─ auto_train.py
│   │   ├─ clean_data.py
│   │   └─ update_model.py
├─ Chrome Extension/
│   ├─ manifest.json
│   ├─ background.js
│   ├─ content_script.js
│   ├─ popup.html
│   └─ popup.js
├─ dataset/
│   ├─ news_data.csv
│   ├─ clean_news_data.csv
├─ requirements.txt
├─ LICENSE
├─ README.md
```

---

## 📥 **Installation Guide**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/wxnxthxn/Machine-Learning-Fake-News-Detection.git
cd fake-news-detection
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the FastAPI Server
```bash
uvicorn app:app --reload
```
- The API will be available at `http://127.0.0.1:8000`
- Check the interactive API docs at `http://127.0.0.1:8000/docs`
---

## 🔥 **API Usage**

### 1️⃣ **POST /check** (Detect Fake News)

#### Response (JSON):
```json
{
  "ai_score": 87.5,
  "google_fact_check": null,
  "source": "Hybrid (ThaiBERT + Google Fact Check)"
}
```
- **ai_score**: The likelihood (0-100%) that the news is real.
- **source**: The model and method used for classification.

---
## 📊 **Model Training**

### 1️⃣ Dataset Cleaning
- Uses `clean_data.py` to preprocess news data (`news_data.csv`).
- Maps `real → 0` and `fake → 1`, removes NaNs, and normalizes text.

### 2️⃣ Feature Engineering (TF-IDF)
- Extracts key features from news content using `TfidfVectorizer`.

### 3️⃣ Model Training & Evaluation
- Trains a **ThaiBERT classifier** (`auto_train.py`).
- Evaluates **accuracy, precision, recall, and confusion matrix**.

### 4️⃣ Saving the Model
- Saves the trained model as **model_latest.pth** for deployment.

---
## Chrome Extension

- See the `Chrome Extension/` folder.  
- Load it in Chrome via `chrome://extensions/`, **Enable Developer Mode**, then **Load Unpacked** → select `Chrome Extension/`.  
- Right-click any highlighted text → “ตรวจสอบข่าวปลอม” to check for fake news.

---

## API Endpoints

**POST** `/check`

- **Body**: `{"text": "..."} or {"url": "..."}`  
- **Response**:
  ```json
  {
    "ai_score": 85.0,
    "google_fact_check": null,
    "source": "Hybrid (ThaiBERT + Google Fact Check)"
  }
  ```
- The `ai_score` indicates how “real” the news is (0-100%).

---
## 📌 **Future Improvements**

🚀 Improve model accuracy with **fine-tuned transformers**  
🚀 Develop a **real-time browser extension** for fake news detection  
🚀 Expand **dataset** with more diverse and multilingual news sources  
🚀 Implement **fact-checking integrations** (e.g., Google Fact Check API)  
---

## 🤝 Contributing
👤 Winithon (Project Lead)
👥 Thitinan (AI Specialist & Document Writer)

1. Fork this repo  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/my-new-feature
   ```  
3. Commit and push your changes  
4. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).  
Copyright (c) 2025 [Winithon Chobchit], [Thitinan Grabthong]
