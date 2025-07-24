let activeTimeframe = '1d';

document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplaySignals(activeTimeframe);
});

function changeTimeframe(newTimeframe, clickedButton) {
    activeTimeframe = newTimeframe;
    document.querySelectorAll('.timeframe-selector button').forEach(button => {
        button.classList.remove('active');
    });
    clickedButton.classList.add('active');
    fetchAndDisplaySignals(activeTimeframe);
}

async function fetchAndDisplaySignals(timeframe) {
    const apiUrl = `https://moedas-production.up.railway.app/signals_v2?timeframe=${timeframe}`;
    const container = document.getElementById('signals-container' );
    container.innerHTML = `<p class="loading-message">Analisando o timeframe de ${timeframe}... ⏳</p>`;

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erro na API: ${response.statusText}`);
        }
        const signals = await response.json();
        container.innerHTML = '';

        if (signals.length === 0) {
            container.innerHTML = '<p>Nenhum sinal encontrado para este timeframe.</p>';
            return;
        }

        signals.forEach(signal => {
            const card = document.createElement('div');
            card.className = 'grid-item';
            let signalColor = '#6c757d';
            const signalText = signal.signal;
            if (signalText.includes('BUY') || signalText.includes('Alta')) {
                signalColor = '#28a745';
            } else if (signalText.includes('SELL') || signalText.includes('Baixa')) {
                signalColor = '#dc3545';
            }
            card.innerHTML = `
                <h3>${signal.pair}</h3>
                <p class="signal-text" style="color: ${signalColor}; font-weight: bold;">${signalText}</p>
                <div class="details">
                    <p><strong>Entrada:</strong> ${signal.entry.toFixed(4)}</p>
                    <p><strong>Stop:</strong> ${signal.stop.toFixed(4)}</p>
                    <p><strong>Target:</strong> ${signal.target.toFixed(4)}</p>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Falha ao buscar sinais:", error);
        container.innerHTML = `<p class="error-message">Ops! Falha ao carregar sinais. ${error.message}</p>`;
    }
}```

---

Depois de colocar cada código no seu devido lugar dentro do branch `feature/timeframes`, o próximo passo será configurar a Railway e a Netlify para fazerem o deploy a partir das pastas e do branch corretos.

Estou aqui para ajudar nessa configuração assim que você terminar de organizar os ficheiros.
