// Espera o HTML da página carregar completamente antes de executar o script
document.addEventListener('DOMContentLoaded', () => {
    // Encontra os elementos na página
    const loginButton = document.getElementById('login-button');
    const passwordInput = document.getElementById('password');

    // Verifica se o botão de login existe antes de adicionar o evento
    if (loginButton) {
        loginButton.addEventListener('click', login);
    } else {
        console.error("Erro: Botão de login com id 'login-button' não foi encontrado.");
    }

    // Verifica se o campo de senha existe antes de adicionar o evento
    if (passwordInput) {
        passwordInput.addEventListener('keyup', function(event) {
            // Se a tecla pressionada for "Enter", tenta fazer o login
            if (event.key === 'Enter') {
                login();
            }
        });
    } else {
        console.error("Erro: Campo de senha com id 'password' não foi encontrado.");
    }
});

// Função que realiza o login
function login() {
    const correctPassword = "Zoe1001";
    const passwordInput = document.getElementById('password');
    const enteredPassword = passwordInput ? passwordInput.value : '';

    const loginSection = document.getElementById('login-section');
    const signalsSection = document.getElementById('signals-section');
    const errorMessage = document.getElementById('error-message');

    if (enteredPassword === correctPassword) {
        // Esconde a seção de login e mostra a de sinais
        if (loginSection) loginSection.style.display = 'none';
        if (signalsSection) signalsSection.style.display = 'block';
        
        // Chama a função para buscar os sinais da API
        fetchSignals();
    } else {
        // Mostra a mensagem de erro de senha
        if (errorMessage) errorMessage.style.display = 'block';
    }
}

// Função que busca os dados da API e preenche a tabela
async function fetchSignals() {
    const apiUrl = "https://moedas-production.up.railway.app/signals";
    const tableBody = document.querySelector("#signals-table tbody" );
    const loadingIndicator = document.getElementById('loading');
    const signalsTable = document.getElementById('signals-table');

    // Mostra "Carregando..."
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (signalsTable) signalsTable.style.display = 'none';

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error(`Erro na API: ${response.statusText}`);
        
        const signals = await response.json();

        if (tableBody) tableBody.innerHTML = ''; // Limpa a tabela

        signals.forEach(signal => {
            const row = document.createElement('tr');
            
            // Lógica de cores
            let signalColor = '#6c757d'; // Cinza padrão
            const signalText = signal.signal;
            if (signalText.includes('BUY') || signalText.includes('Alta')) signalColor = '#28a745'; // Verde
            else if (signalText.includes('SELL') || signalText.includes('Baixa')) signalColor = '#dc3545'; // Vermelho

            // Preenche a linha da tabela
            row.innerHTML = `
                <td>${signal.pair}</td>
                <td>${signal.entry.toFixed(4)}</td>
                <td style="font-weight: bold; color: ${signalColor};">${signalText}</td>
                <td>${signal.stop.toFixed(4)}</td>
                <td>${signal.target.toFixed(4)}</td>
            `;
            if (tableBody) tableBody.appendChild(row);
        });

        // Esconde "Carregando..." e mostra a tabela
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        if (signalsTable) signalsTable.style.display = 'table';

    } catch (error) {
        console.error("Falha ao buscar sinais:", error);
        if (loadingIndicator) {
            loadingIndicator.textContent = "Erro ao carregar os sinais.";
            loadingIndicator.style.color = "#dc3545";
        }
    }
}

