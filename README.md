🔮 Crypton Signals Frontend

Interface moderna e segura para visualização de sinais de criptomoedas. Desenvolvido com HTML, CSS e JavaScript puro, pronto para deploy no Netlify.


---

📦 Funcionalidades

🔐 Acesso protegido por senha (Zoe1001)

📊 Exibição de múltiplos sinais (BTC, ETH, XRP)

🌙 Visual escuro moderno e responsivo

⚡ Integração com API real via Railway



---

🌐 Link da API Backend

Certifique-se de que o backend esteja rodando em:

https://moedas-production.up.railway.app/signals

> Esse endpoint deve retornar um array de sinais no formato:



[
  {
    "pair": "BTC/USDT",
    "entry": 57432.12,
    "target": 59000.00,
    "stop": 56200.00,
    "signal": "BUY"
  }
]


---

🚀 Deploy no Netlify

1. Crie uma conta gratuita em https://app.netlify.com


2. Clique em "Add new site" → "Import from Git"


3. Escolha seu repositório GitHub (ex: crypton-signals-frontend)


4. Configure como site estático:

Build command: deixe em branco

Publish directory: public



5. Clique em Deploy ✅




---

🛠️ Estrutura de Pastas

crypton-frontend/
└── public/
    ├── index.html     # Estrutura principal
    ├── style.css      # Visual moderno e dark mode
    ├── app.js         # Lógica de fetch e login por senha
    └── logo.png       # Logo do projeto


---

📍 Observações

A senha está embutida no frontend para fins simples: Zoe1001

Para uso profissional, considere um backend com autenticação real (JWT ou similar).



---

👨‍💻 Autor

Desenvolvido por David Danubio com suporte do ChatGPT 🧠


---

Pronto para Netlify. Boa sorte com o projeto! 🚀

