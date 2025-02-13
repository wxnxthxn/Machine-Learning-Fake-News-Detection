chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "SHOW_RESULT") {
        chrome.storage.local.set({ analysis: message.result }, () => {
            console.log("✅ ข้อมูลถูกบันทึกลง Storage แล้ว");
            chrome.action.openPopup();
        });
    }

    if (message.type === "SHOW_ERROR") {
        alert(message.message);
    }
});
