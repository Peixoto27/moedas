// O nome da função deve ser exatamente "checkPassword", como está no seu HTML.
function checkPassword() {
    const correctPassword = "Zoe1001";
    const enteredPassword = document.getElementById('password-input').value; // O ID correto do seu input

    const loginScreen = document.getElementById('login-screen'); // A tela de login
    const appContent = document.getElementById('app');           // O conteúdo principal do app

    if (enteredPassword === correctPassword) {
        // Se a senha estiver correta, esconde a tela de login e mostra o app
        loginScreen.style.display = 'none';
        appContent.style.display = 'block';
        
        // Chama a função para buscar e exibir os sinais
        fetchAndDisplaySignals();
    } else {
        // Se a senha estiver errada, podemos dar um feedback visual
        alert("Senha incorreta!"); // Um alerta simples é eficaz
        document.getElementById('password-input').value = ''; // Limpa o campo
    }
}

// Função para buscar os dados da API e criar os cards de sinais
async function fetchAndDisplaySignals() {
    const apiUrl = "https://moedas-production.up.railway.app/signals";
    const container = document.getElementById('signals-container' ); // O container onde os sinais serão inseridos

    // Mostra uma mensagem de "Carregando..." dentro do container
    container.innerHTML = '<p class="loading-message">Buscando os melhores sinais na galáxia... 🚀</p>';

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`A API não respondeu como esperado: ${response.statusText}`);
        }
        const signals = await response.json();

        // Limpa a mensagem de "Carregando..."
        container.innerHTML = '';

        // Cria um card para cada sinal recebido
        signals.forEach(signal => {
            // Cria o elemento do card
            const card = document.createElement('div');
            card.className = 'grid-item'; // Usa a classe do seu CSS

            // Define a cor baseada no sinal
            let signalColor = '#6c757d'; // Cinza (padrão para HOLD/NEUTRAL)
            const signalText = signal.signal;
            if (signalText.includes('BUY') || signalText.includes('Alta')) {
                signalColor = '#28a745'; // Verde
            } else if (signalText.includes('SELL') || signalText.includes('Baixa')) {
                signalColor = '#dc3545'; // Vermelho
            }

            // Preenche o conteúdo do card com os dados do sinal
            card.innerHTML = `
                <h3>${signal.pair}</h3>
                <p class="signal-text" style="color: ${signalColor}; font-weight: bold;">${signalText}</p>
                <div class="details">
                    <p><strong>Entrada:</strong> ${signal.entry.toFixed(4)}</p>
                    <p><strong>Stop:</strong> ${signal.stop.toFixed(4)}</p>
                    <p><strong>Target:</strong> ${signal.target.toFixed(4)}</p>
                </div>
            `;

            // Adiciona o card criado ao container na página
            container.appendChild(card);
        });

    } catch (error) {
        console.error("Falha ao buscar sinais:", error);
        // Mostra uma mensagem de erro amigável no container
        container.innerHTML = '<p class="error-message">Ops! Não foi possível carregar os sinais. Tente novamente mais tarde.</p>';
    }
}
