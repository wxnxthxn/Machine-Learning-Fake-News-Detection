document.addEventListener('DOMContentLoaded', function () {
    console.log("📌 Popup Loaded: กำลังดึงข้อมูลจาก Storage");

    chrome.storage.local.get(['analysis'], function (data) {
        console.log("📌 ดึงข้อมูลจาก Storage:", data);

        if (data.analysis) {
            // อ้างอิง element ที่ต้องใช้งาน
            const analysisElement = document.getElementById('result-analysis');
            const bannerElement = document.getElementById('result-banner');
            const scoreElement = document.getElementById('result-score');

            // ตั้งค่าผลลัพธ์ (Label) โดยอิงจากคะแนนที่ได้จากโมเดล
            analysisElement.innerText = getLabel(data.analysis.ai_score);

            // ตั้งค่าภาพ Banner ตามประเภทข่าว
            bannerElement.src = getBanner(data.analysis.ai_score);

            // แสดงโอกาสที่เป็นข่าวจริง (คะแนน)
            scoreElement.innerText = data.analysis.ai_score.toFixed(2);
        } else {
            console.error("⚠️ ไม่พบข้อมูลจาก Storage");
        }
    });

    document.getElementById('close-popup').addEventListener('click', () => window.close());
});

// ฟังก์ชันเลือกไอคอนแบนเนอร์ที่เหมาะสม (แบ่งเป็น 4 ประเภท)
// - ข่าวจริง: score ≥ 80
// - ข่าวไม่น่าเชื่อถือ: 50 ≤ score < 80
// - ข่าวลือ: 25 ≤ score < 50
// - ข่าวปลอม: score < 25
function getBanner(score) {
    if (score >= 80) {
        return chrome.runtime.getURL('banner/correct.PNG');
    } else if (score >= 50) {
        return chrome.runtime.getURL('banner/warning.PNG');
    } else if (score >= 25) {
        return chrome.runtime.getURL('banner/suspicious.png');
    } else {
        return chrome.runtime.getURL('banner/incorrect.PNG');
    }
}

// ฟังก์ชันกำหนดข้อความแสดงผลตามคะแนน (4 ประเภท)
function getLabel(score) {
    if (score >= 80) {
        return '✅ ข่าวจริง';
    } else if (score >= 50) {
        return '⚠️ ข่าวไม่น่าเชื่อถือ';
    } else if (score >= 25) {
        return '🔍 ข่าวลือ';
    } else {
        return '❌ ข่าวปลอม';
    }
}
