// background.js

chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "check-text",
        title: "ตรวจสอบข่าวปลอม",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === "check-text" && info.selectionText) {
        const textToCheck = info.selectionText.trim();
        const API_URL = "http://your-server-ip:8000/check"; // เปลี่ยนเป็นเซิร์ฟเวอร์จริง

        console.log("📤 ส่งข้อความไปตรวจสอบ:", textToCheck);

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: textToCheck })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const result = await response.json();
            console.log("✅ ผลลัพธ์จาก API:", result);

            // ส่งผลลัพธ์ให้ content_script.js แสดงผล
            chrome.tabs.sendMessage(tab.id, { type: "SHOW_RESULT", result: result });

        } catch (error) {
            console.error("🚨 เชื่อมต่อกับเซิร์ฟเวอร์ไม่ได้:", error);

            // แจ้งเตือนผู้ใช้
            chrome.tabs.sendMessage(tab.id, { type: "SHOW_ERROR", message: "❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ กรุณาลองใหม่" });
        }
    }
});
