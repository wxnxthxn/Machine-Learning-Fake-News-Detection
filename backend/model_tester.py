from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# ✅ โหลดโมเดล
MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.pth")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

def predict(text):
    """ รับข้อความข่าวแล้วคืนค่าความน่าเชื่อถือ (0-100%) """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    score = torch.softmax(logits, dim=1)[0][1].item()
    return (1 - score) * 100  # เปลี่ยนเป็นเปอร์เซ็นต์ข่าวจริง

# ✅ ทดสอบการทำงาน
if __name__ == "__main__":
    text = "นายกรัฐมนตรีให้สัมภาษณ์เรื่องเศรษฐกิจล่าสุด"
    print(f"โอกาสที่เป็นข่าวจริง: {predict(text)}%")
