chrome.runtime.onInstalled.addListener(() => {
    console.log("🚀 Extension Installed: สร้างเมนูคลิกขวา");

    chrome.contextMenus.create({
        id: "check-text",
        title: "ตรวจสอบข่าวปลอม",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === "check-text" && info.selectionText) {
        const textToCheck = info.selectionText.trim();

        // กำหนดความยาวขั้นต่ำของข้อความที่ต้องเลือก (ตัวอย่าง ใช้ 100 ตัวอักษร)
        const MIN_TEXT_LENGTH = 100;
    if (textToCheck.length < MIN_TEXT_LENGTH) {
        const selectedLength = textToCheck.length;
        const missingChars = MIN_TEXT_LENGTH - selectedLength;
    chrome.tabs.sendMessage(tab.id, {
        type: "SHOW_ERROR",
        message: `ข้อความที่เลือกมีความยาว ${selectedLength} ตัวอักษร กรุณาเลือกเพิ่มอีก ${missingChars} ตัวอักษร เพื่อให้ครบ ${MIN_TEXT_LENGTH} ตัวอักษร`
    });
    return;
    }


        const API_URL = "http://localhost:80000/check";

        console.log("📤 ส่งข้อมูลไปที่เซิร์ฟเวอร์:", JSON.stringify({ text: textToCheck }));

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: textToCheck })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status} - ${await response.text()}`);
            }

            const result = await response.json();
            console.log("✅ ผลลัพธ์จาก API:", result);

            // บันทึกข้อมูลลง storage ให้ popup ใช้งาน
            chrome.storage.local.set({ analysis: result }, () => {
                console.log("✅ ผลลัพธ์ถูกบันทึกลง Storage");
                // เปิด popup
                chrome.action.openPopup();
            });

            // ส่งข้อมูลไปยัง content_script.js
            chrome.scripting.executeScript({
                target: { tabId: tab.id },
                files: ["content_script.js"]
            }, () => {
                if (chrome.runtime.lastError) {
                    console.error("🚨 โหลด content_script.js ไม่สำเร็จ:", chrome.runtime.lastError.message);
                } else {
                    console.log("✅ content_script.js ถูกโหลดแล้ว");
                    chrome.tabs.sendMessage(tab.id, { type: "SHOW_RESULT", result: result });
                }
            });

        } catch (error) {
            console.error("🚨 เชื่อมต่อกับเซิร์ฟเวอร์ไม่ได้:", error);
            chrome.tabs.sendMessage(tab.id, {
                type: "SHOW_ERROR",
                message: "❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ กรุณาลองใหม่"
            });
        }
    }
});
