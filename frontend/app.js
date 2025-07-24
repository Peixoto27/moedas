const API_URL = "https://moedas-production.up.railway.app/signals";
const PASSWORD = "Zoe1001";

function checkPassword() {
  const input = document.getElementById("password-input");
  if (input.value === PASSWORD) {
    document.getElementById("login-screen").style.display = "none";
    document.getElementById("app").style.display = "block";
    fetchSignals();
  } else {
    alert("Senha incorreta!");
  }
}

function fetchSignals() {
  fetch(API_URL)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("signals-container");
      container.innerHTML = "";
      data.forEach(signal => {
        const card = document.createElement("div");
        card.className = "card";
        const signalColor = signal.signal === "BUY" ? "green" : "red";
        card.innerHTML = `
          <h2>📊 ${signal.pair}</h2>
          <p><strong>Entrada:</strong> ${signal.entry.toFixed(2)}</p>
          <p><strong>Alvo:</strong> ${signal.target.toFixed(2)}</p>
          <p><strong>Stop:</strong> ${signal.stop.toFixed(2)}</p>
          <p><strong>Sinal:</strong> <span style="color:${signalColor}; font-weight:bold">${signal.signal}</span></p>
        `;
        container.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Erro ao carregar os sinais", err);
      document.getElementById("signals-container").innerHTML = "<p>Erro ao carregar os sinais.</p>";
    });
}