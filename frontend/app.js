// Encontra o elemento que mostra o sinal
const signalElement = document.getElementById('signal-display');

// Pega o texto do sinal vindo da API
const signalText = data.signal; // ex: "HOLD (Tendência de Alta)"

signalElement.textContent = signalText;

// --- LÓGICA DE CORES CORRIGIDA ---

// Removemos a classe de cor anterior para garantir que não haja conflitos
signalElement.classList.remove('signal-buy', 'signal-sell', 'signal-hold');

// Verificamos o conteúdo do texto do sinal
if (signalText.includes('BUY') || signalText.includes('Alta')) {
  // Se contiver "BUY" OU "Alta", fica verde
  signalElement.classList.add('signal-buy'); // Usar classes CSS é melhor
  // ou signalElement.style.color = '#28a745'; // Verde

} else if (signalText.includes('SELL') || signalText.includes('Baixa')) {
  // Se contiver "SELL" OU "Baixa", fica vermelho
  signalElement.classList.add('signal-sell');
  // ou signalElement.style.color = '#dc3545'; // Vermelho

} else {
  // Para qualquer outro caso (como "NEUTRAL" ou "ERROR")
  signalElement.classList.add('signal-hold');
  // ou signalElement.style.color = '#6c757d'; // Cinza
}
