async function fetchSignals() {
  try {
    const response = await fetch("https://moedas-production.up.railway.app/signals");
    const data = await response.json();

    const container = document.getElementById("signals-container");
    container.innerHTML = "";

    data.forEach(signal => {
      const card = document.createElement("div");
      card.className = "card";

      const signalColor = signal.signal === "BUY" ? "green" : "red";

      card.innerHTML = `
        <h2>📊 Sinal de Cripto</h2>
        <p><strong>Par:</strong> ${signal.pair}</p>
        <p><strong>Entrada:</strong> ${signal.entry.toFixed(2)}</p>
        <p><strong>Alvo:</strong> ${signal.target.toFixed(2)}</p>
        <p><strong>Stop:</strong> ${signal.stop.toFixed(2)}</p>
        <p><strong>Sinal:</strong> <span style="color:${signalColor}">${signal.signal}</span></p>
      `;
      container.appendChild(card);
    });

  } catch (error) {
    console.error("Erro ao buscar sinais:", error);
    document.getElementById("signals-container").innerHTML = "<p>Erro ao carregar os sinais.</p>";
  }
}

document.addEventListener("DOMContentLoaded", fetchSignals);
