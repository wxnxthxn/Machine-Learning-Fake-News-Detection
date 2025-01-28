// background.js

// เมื่อ Extension ถูกติดตั้งหรืออัปเดต (ในกรณี Manifest V3, จะใช้ Service Worker แทน background page เดิม)
chrome.runtime.onInstalled.addListener(() => {
  // สร้าง Context Menu สำหรับกรณีที่ผู้ใช้ไฮไลต์ข้อความ
  chrome.contextMenus.create({
    id: "check-text",        // ค่า ID ไว้อ้างอิงใน onClicked
    title: "Check fake news",// ข้อความที่จะแสดงในเมนูคลิกขวา
    contexts: ["selection"]  // แสดงเมนูเฉพาะตอนไฮไลต์ข้อความ
  });
});

// เมื่อ Context Menu ถูกคลิก
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  // ตรวจสอบว่าคลิกเมนู "check-text" และมีข้อความไฮไลต์
  if (info.menuItemId === "check-text" && info.selectionText) {
    const textToCheck = info.selectionText.trim(); // ตัดช่องว่างหัวท้าย

    // ถ้าข้อความหลัง trim ยังว่างเปล่า ให้ยกเลิก
    if (!textToCheck) {
      console.warn("No text selected or empty string.");
      return;
    }

    console.log("Context menu clicked with text:", textToCheck);

    try {
      // เรียก API ที่ Backend (สมมติรันที่ localhost:8000)
      const response = await fetch("http://localhost:8000/check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: textToCheck })
      });

      // เช็คสถานะการตอบกลับจากเซิร์ฟเวอร์
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // แปลงผลลัพธ์เป็น JSON
      const result = await response.json();

      console.log("Received result from backend:", result);

      // ส่งผลลัพธ์ให้ content_script.js แสดงผล
      chrome.tabs.sendMessage(tab.id, {
        type: "SHOW_RESULT",
        result: result
      }, (res) => {
        // Callback หลังส่ง message เสร็จ
        if (chrome.runtime.lastError) {
          // ถ้าเกิด error ในการส่ง message
          console.error("Failed to send message to content script:", chrome.runtime.lastError.message);
        } else {
          console.log("Message sent successfully. Content script response:", res);
        }
      });

    } catch (err) {
      // หากการ fetch หรือ parse JSON เกิดข้อผิดพลาด
      console.error("Error checking text:", err);

      // ส่ง message ไป content script แจ้ง Error ให้ผู้ใช้
      chrome.tabs.sendMessage(tab.id, {
        type: "SHOW_ERROR",
        message: "Cannot check the highlighted text right now. Please try again later."
      });
    }
  }
});
