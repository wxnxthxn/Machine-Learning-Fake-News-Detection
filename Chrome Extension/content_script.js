// เพิ่มบรรทัดนี้ไว้ต้นไฟล์ content_script.js
console.log("content_script.js has been injected!");

// ส่วนฟังข้อความจาก background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Log เพื่อดูว่าเราได้รับ message อะไร
  console.log("Received message in content script:", message);

  if (message.type === "SHOW_RESULT") {
    // สร้าง DOM element แสดงผลลัพธ์บนหน้า
    const div = document.createElement('div');
    div.style.position = 'fixed';
    div.style.top = '20px';
    div.style.right = '20px';
    div.style.padding = '10px';
    div.style.background = '#fff';
    div.style.border = '1px solid #ccc';
    div.style.zIndex = '99999';
    div.innerHTML = `
      <h4>Fake News Checker Result</h4>
      <p>Score: ${message.result.score.toFixed(2)}%</p>
      <p>${message.result.explanation}</p>
      <h5>Recommendations:</h5>
      <ul>
        ${message.result.recommendations.map(r => `<li><a href="${r.url}" target="_blank">${r.title}</a></li>`).join('')}
      </ul>
      <button id="close-fake-news-box">Close</button>
    `;
    document.body.appendChild(div);
    div.querySelector('#close-fake-news-box').addEventListener('click', () => {
      div.remove();
    });
  }

  // (ตัวเลือก) หากอยากส่ง response กลับ
  sendResponse({ status: "OK, content script got the message" });

  // ต้อง return true หากเราใช้ sendResponse แบบ async (Chrome MV3)
  // return true;
});
