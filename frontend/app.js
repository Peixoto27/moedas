document.addEventListener("DOMContentLoaded", () => {
  fetch("https://moedas-production.up.railway.app/signals")
    .then(response => {
      if (!response.ok) {
        throw new Error("Erro na resposta da API");
      }
      return response.json();
    })
    .then(data => {
      const signalElement = document.getElementById("signals");

      if (!signalElement) {
        console.error("Elemento #signals não encontrado.");
        return;
      }

      signalElement.innerHTML = `
        <div style="padding: 20px; background-color: #121212; border-radius: 12px; color: white;">
          <h2>📊 Sinal de Cripto</h2>
          <p><strong>Par:</strong> ${data.pair}</p>
          <p><strong>Entrada:</strong> ${data.entry}</p>
          <p><strong>Alvo:</strong> ${data.target}</p>
          <p><strong>Stop:</strong> ${data.stop}</p>
          <p><strong>Sinal:</strong> <span style="color: ${data.signal === 'BUY' ? 'green' : 'red'}">${data.signal}</span></p>
        </div>
      `;
    })
    .catch(error => {
      console.error("Erro ao buscar os sinais:", error);
      const signalElement = document.getElementById("signals");
      if (signalElement) {
        signalElement.innerHTML = `<p style="color:red;">Erro ao carregar os sinais. Tente novamente mais tarde.</p>`;
      }
    });
});
