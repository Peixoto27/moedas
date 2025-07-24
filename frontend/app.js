// Função principal que é chamada quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('login-button'); // Assumindo que o botão de login tem id="login-button"
    const passwordInput = document.getElementById('password');   // Assumindo que o campo de senha tem id="password"

    // Adiciona o evento de clique ao botão de login
    if (loginButton) {
        loginButton.addEventListener('click', login);
    }

    // Adiciona o evento de "Enter" ao campo de senha
    if (passwordInput) {
        passwordInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                login();
            }
        });
    }
});

// --- LÓGICA DE LOGIN ---
function login() {
    const correctPassword = "Zoe1001";
    const enteredPassword = document.getElementById('password').value;
    const loginSection = document.getElementById('login-section'); // A div/seção de login
    const signalsSection = document.getElementById('signals-section'); // A div/seção dos sinais
    const errorMessage = document.getElementById('error-message'); // O elemento para mostrar erro de senha

    if (enteredPassword === correctPassword) {
        // Esconde a seção de login e mostra a seção de sinais
        if (loginSection) loginSection.style.display = 'none';
        if (signalsSection) signalsSection.style.display = 'block';
        
        fetchSignals(); // Chama a função para buscar os sinais
    } else {
        // Mostra a mensagem de erro
        if (errorMessage) errorMessage.style.display = 'block';
    }
}

// --- LÓGICA PARA BUSCAR E EXIBIR OS SINAIS ---
async function fetchSignals() {
    const apiUrl = "https://moedas-production.up.railway.app/signals";
    const tableBody = document.querySelector("#signals-table tbody" ); // O corpo da sua tabela de sinais
    const loadingIndicator = document.getElementById('loading'); // Um elemento para mostrar "Carregando..."
    const signalsTable = document.getElementById('signals-table'); // A tabela em si

    // Mostra o indicador de "Carregando..." e esconde a tabela
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (signalsTable) signalsTable.style.display = 'none';

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`Erro na rede: ${response.statusText}`);
        }
        const signals = await response.json();

        // Limpa o corpo da tabela antes de adicionar novas linhas
        if (tableBody) tableBody.innerHTML = ''; 

        signals.forEach(signal => {
            const row = document.createElement('tr');

            // --- LÓGICA DE CORES ---
            let signalColor = '#6c757d'; // Cor padrão (cinza)
            const signalText = signal.signal; // O texto do sinal, ex: "HOLD (Tendência de Alta)"

            if (signalText.includes('BUY') || signalText.includes('Alta')) {
                signalColor = '#28a745'; // Verde
            } else if (signalText.includes('SELL') || signalText.includes('Baixa')) {
                signalColor = '#dc3545'; // Vermelho
            }

            // Cria as células da tabela com os dados e a cor correta
            row.innerHTML = `
                <td>${signal.pair}</td>
                <td>${signal.entry.toFixed(4)}</td>
                <td style="font-weight: bold; color: ${signalColor};">${signalText}</td>
                <td>${signal.stop.toFixed(4)}</td>
                <td>${signal.target.toFixed(4)}</td>
            `;
            if (tableBody) tableBody.appendChild(row);
        });

        // Esconde o "loading" e mostra a tabela preenchida
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        if (signalsTable) signalsTable.style.display = 'table';

    } catch (error) {
        console.error("Falha ao buscar sinais:", error);
        if (loadingIndicator) {
            loadingIndicator.textContent = "Erro ao carregar os sinais. Tente mais tarde.";
            loadingIndicator.style.color = "#dc3545";
        }
    }
}
