document.getElementById('check-btn').addEventListener('click', async () => {
  const url = document.getElementById('url-input').value.trim();
  if (!url) return;

  const response = await fetch("http://localhost:8000/check", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({url: url})
  });
  const result = await response.json();
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = `
    <h4>Result</h4>
    <p>Score: ${result.score.toFixed(2)}%</p>
    <p>${result.explanation}</p>
    <h5>Recommendations:</h5>
    <ul>
      ${result.recommendations.map(r => `<li><a href="${r.url}" target="_blank">${r.title}</a></li>`).join('')}
    </ul>
  `;
});
