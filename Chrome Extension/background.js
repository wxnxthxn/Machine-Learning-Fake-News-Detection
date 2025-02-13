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
        const API_URL = "http://localhost:8000/check"; // ✅ เปลี่ยนให้เรียก localhost

        console.log("📤 ส่งข้อมูลไปที่เซิร์ฟเวอร์:", JSON.stringify({ text: textToCheck }));
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000); // ✅ ตั้ง Timeout 8 วินาที

            const response = await fetch(API_URL, {
                 method: "POST",
                 headers: { "Content-Type": "application/json" },
                 body: JSON.stringify({ text: textToCheck })
            });
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status} - ${await response.text()}`);
            }

            const result = await response.json();
            console.log("✅ ผลลัพธ์จาก API:", result);

            // ส่งผลลัพธ์ให้ content_script.js แสดงผล
            chrome.tabs.sendMessage(tab.id, { type: "SHOW_RESULT", result: result });

        } catch (error) {
            console.error("🚨 เชื่อมต่อกับเซิร์ฟเวอร์ไม่ได้:", error);

            let errorMessage = "❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ กรุณาลองใหม่";
            if (error.name === "AbortError") {
                errorMessage = "⏳ การเชื่อมต่อใช้เวลานานเกินไป กรุณาลองใหม่";
            } else if (error.message.includes("422")) {
                errorMessage = "⚠️ ไม่สามารถประมวลผลข้อมูลที่ส่งมาได้";
            }

            // แจ้งเตือนผู้ใช้
            chrome.tabs.sendMessage(tab.id, { type: "SHOW_ERROR", message: errorMessage });
        }
    }
});
