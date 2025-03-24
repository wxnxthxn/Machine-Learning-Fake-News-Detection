 ### `📰 Machine Learning Fake News Detection`

 ## 🔍 **Project Overview**
This project provides a **Chrome Extension** and a **FastAPI** backend to detect fake news based on text. It uses a trained **ThaiBERT (WangchanBERTa) model** to classify news as *real* or *fake*. The system can also give a trust score and explanations.

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

✅ Classifies news articles as **Real or Fake** based on highlighted text input.  
✅ Utilizes a **ThaiBERT (WangchanBERTa) model** for predictions.  
✅ Provides a **FastAPI-based REST API** for integration with the Chrome Extension.  
✅ Outputs a trust score along with a simple result label (e.g., ✅ ข่าวจริง).

---
## 🛠 **Tech Stack**
- **Programming Language:** Python, JavaScript, HTML, CSS
- **Framework:** FastAPI
- **Machine Learning Model:** ThaiBERT (WangchanBERTa) for text classification
- **Browser Extension:** Chrome Extension API, JavaScript
- **Deployment & Storage:** GitHub (code only; model files are handled separately due to size)
- **Data Processing:** Pandas, PyTorch, Transformers
- **Storage & Deployment:** GitHub, Model Persistence
---
## Architecture

```bash
ProjectMLFakeNewsDetection/
├─ backend/
│   ├─ app.py                 # FastAPI backend API for text classification
│   ├─ model/
│   │   ├─ model_latest.pth   # Latest trained ThaiBERT model (not pushed to GitHub)
│   │   └─ update_model.py     # Script to update the model used by the API
│   ├─ training/
│   │   ├─ auto_train.py       # Script for training the ThaiBERT model
│   │   ├─ clean_data.py       # Script for cleaning and preprocessing the dataset
│   │   └─ model_tester.py     # Script for testing the ThaiBERT model
├─ Chrome Extension/
├─ banner/
│   │   ├─ correct.PNG # Banner Real news
│   │   ├─ incorrect.PNG # Banner Fake news
│   │   ├─ suspicious.PNG # Banner Rumor news
│   │   └─ warning.PNG # Banner Unreliable news
│   ├─ manifest.json          # Chrome Extension manifest
│   ├─ background.js          # Background script handling context menu and API calls
│   ├─ content_script.js      # Content script for in-page interactions
│   ├─ popup.html             # Popup UI for displaying analysis results
│   └─ popup.js               # Script for handling popup UI logic
├─ dataset/
│   ├─ news_data.csv          # Raw news dataset
│   └─ clean_news_data.csv    # Cleaned news dataset for training
├─ requirements.txt           # Python dependencies
├─ LICENSE
└─ README.md

```

---

## 📥 **Installation Guide**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/wxnxthxn/Machine-Learning-Fake-News-Detection.git
cd Machine-Learning-Fake-News-Detection
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the FastAPI Server
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8001 --reload
```
- The API will be available at `http://127.0.0.1:8001`
- Check the interactive API docs at `http://127.0.0.1:8001/docs`
---

## 🔥 **API Usage**

### 1️⃣ **POST /check** (Detect Fake News)

#### Response (JSON):
```json
{
  "source": "ThaiBERT",
  "ai_score": 87.5
}
```
- **ai_score**: Indicates the likelihood (0-100%) that the news is real.
- **source**: The model used for prediction (ThaiBERT).

## 📊 **Model Training**

### 1️⃣ Dataset Cleaning
- Run `clean_data.py` to preprocess the raw dataset (`news_data.csv`)and generate (`clean_news_data.csv`).
```bash
python backend/training/clean_data.py
```

### 2️⃣ Model Training
- Run `auto_train.py` to train the ThaiBERT model on the cleaned dataset.
```bash
python backend/training/auto_train.py
```

### 3️⃣ Update Model for Inference
- After training, run `update_model.py` to update the model used by the API.
```bash
python backend/training/update_model.py
```

### 4️⃣ Saving the Model
- Saves the trained model as **model_latest.pth** for deployment.

---
## Chrome Extension

- The Chrome Extension is located in the `Chrome Extension/` folder.
- To install the extension:
  1. Open Chrome and navigate to `chrome://extensions/`
  2. Enable **Developer Mode**
  3. Click **Load Unpacked** and select the `Chrome Extension/` folder.
- To use the extension:
  - Highlight the text on any webpage.
  - Right-click and select **"ตรวจสอบข่าวปลอม"**.
  - The extension will display a popup showing the analysis results.

---

## API Endpoints

**POST** `/check`

- **Body**: `{"text": "..."}`  
  (Note: This API now only accepts a text input from highlighted content.)
- **Response**:
  ```json
  {
    "source": "ThaiBERT",
    "ai_score": 85.0
  }

  ```
- The `ai_score` indicates how “real” the news is (0-100%).

---
## 📌 **Future Improvements**

🚀 Enhance model accuracy with further fine-tuning on diverse datasets.  
🚀 Develop a **real-time browser extension** for fake news detection  
🚀 Expand **dataset** with more diverse and multilingual news sources  
🚀 Integrate additional features for real-time news verification.
---

## 🤝 Contributing
👤 Winithon (Project Lead & Programmer)  
👥 Thitinan (AI Specialist & Document Writer)

1. Fork this repo  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/my-new-feature
   ```  
3. Commit and push your changes  
4. Open a Pull Request
5. Review us on the Chrome Web Store https://chromewebstore.google.com/detail/lajjflehekjcbpjfejmibeobjlomlenp?utm_source=item-share-cp

---

## License

This project is licensed under the [MIT License](LICENSE).  
Copyright (c) 2025 [Winithon Chobchit], [Thitinan Grabthong]
