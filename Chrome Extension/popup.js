document.addEventListener('DOMContentLoaded', function () {
    console.log("📌 Popup Loaded: กำลังดึงข้อมูลจาก Storage");

    chrome.storage.local.get(['analysis'], function (data) {
        console.log("📌 ดึงข้อมูลจาก Storage:", data);

        if (data.analysis) {
            // อ้างอิง element ที่ต้องใช้งาน
            const analysisElement = document.getElementById('result-analysis');
            const bannerElement = document.getElementById('result-banner');
            const scoreElement = document.getElementById('result-score');

            // ตั้งค่าผลลัพธ์
            analysisElement.innerText = getLabel(data.analysis.ai_score);

            // ตั้งค่าภาพ Banner
            bannerElement.src = getBanner(data.analysis.ai_score);

            // แสดงโอกาสที่เป็นข่าวจริง
            scoreElement.innerText = data.analysis.ai_score.toFixed(2);
        } else {
            console.error("⚠️ ไม่พบข้อมูลจาก Storage");
        }
    });

    document.getElementById('close-popup').addEventListener('click', () => window.close());
});

// ฟังก์ชันเลือกไอคอนแบนเนอร์ที่เหมาะสม
function getBanner(score) {
    if (score >= 75) return chrome.runtime.getURL('banner/correct.PNG');
    if (score >= 50) return chrome.runtime.getURL('banner/warning.PNG');
    return chrome.runtime.getURL('banner/incorrect.PNG');
}

// ฟังก์ชันกำหนดข้อความแสดงผล
function getLabel(score) {
    if (score >= 75) return '✅ ข่าวจริง';
    if (score >= 50) return '⚠️ ข่าวไม่น่าเชื่อถือ';
    return '❌ ข่าวปลอม';
}
