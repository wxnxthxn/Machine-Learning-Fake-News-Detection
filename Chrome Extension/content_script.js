chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "SHOW_RESULT") {
        const div = document.createElement('div');
        div.style.position = 'fixed';
        div.style.top = '10px';
        div.style.right = '10px';
        div.style.width = '250px';
        div.style.borderRadius = '8px';
        div.style.overflow = 'hidden';
        div.style.boxShadow = '0px 4px 6px rgba(0,0,0,0.1)';
        div.style.zIndex = '99999';

        div.innerHTML = `
            <img src="${getBanner(message.result.score)}" width="100%">
            <p style="text-align:center;"><strong>โอกาสที่เป็นข่าวจริง:</strong> ${message.result.score.toFixed(2)}%</p>
            <p style="text-align:center;"><strong>ผลลัพธ์:</strong> ${getLabel(message.result.score)}</p>
            <button id="close-fake-news-box" style="display:block;margin:5px auto;">ปิด</button>
        `;

        document.body.appendChild(div);
        div.querySelector('#close-fake-news-box').addEventListener('click', () => {
            div.remove();
        });
    }
});

function getBanner(score) {
    if (score >= 75) return chrome.runtime.getURL('banner/correct.PNG');  // ✅ ข่าวจริง
    if (score >= 50) return chrome.runtime.getURL('banner/warning.PNG');  // ⚠️ ข่าวไม่น่าเชื่อถือ
    return chrome.runtime.getURL('banner/incorrect.PNG');                 // ❌ ข่าวปลอม
}

function getLabel(score) {
    if (score >= 75) return '✅ ข่าวจริง';
    if (score >= 50) return '⚠️ ข่าวไม่น่าเชื่อถือ';
    return '❌ ข่าวปลอม';
}
