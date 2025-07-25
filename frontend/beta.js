// Forçando um novo deploy para aplicar as configurações de diretório.
let activeTimeframe = '1d';

// Função chamada quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
    // Busca os sinais do timeframe padrão ('1d') ao carregar a página
    fetchAndDisplaySignals(activeTimeframe);
});

// Função para mudar o timeframe e buscar novos dados
function changeTimeframe(newTimeframe, clickedButton) {
    // Atualiza o timeframe ativo
    activeTimeframe = newTimeframe;

    // Atualiza o estilo dos botões para mostrar qual está ativo
    document.querySelectorAll('.timeframe-selector button').forEach(button => {
        button.classList.remove('active');
    });
    clickedButton.classList.add('active');

    // Busca os sinais para o novo timeframe
    fetchAndDisplaySignals(activeTimeframe);
}

// Função principal para buscar e exibir os sinais
async function fetchAndDisplaySignals(timeframe) {
    // A URL agora aponta para a nova rota e inclui o parâmetro de timeframe
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
}
