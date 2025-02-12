document.addEventListener('DOMContentLoaded', function () {
    chrome.storage.local.get(['analysis'], function (data) {
        if (data.analysis) {
            document.getElementById('result-confidence').innerText = `โอกาสที่เป็นข่าวจริง: ${data.analysis.score.toFixed(2)}%`;
            document.getElementById('result-text').innerText = getLabel(data.analysis.score);
            document.getElementById('result-banner').src = getBanner(data.analysis.score);
        }
    });

    document.getElementById('close-popup').addEventListener('click', () => window.close());
});

function getBanner(score) {
    if (score >= 75) return 'banner/correct.PNG';  // ✅ ข่าวจริง
    if (score >= 50) return 'banner/warning.PNG';  // ⚠️ ข่าวไม่น่าเชื่อถือ
    return 'banner/incorrect.PNG';                 // ❌ ข่าวปลอม
}

function getLabel(score) {
    if (score >= 75) return '✅ ข่าวจริง';
    if (score >= 50) return '⚠️ ข่าวไม่น่าเชื่อถือ';
    return '❌ ข่าวปลอม';
}
