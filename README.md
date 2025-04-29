# ChatBotCS 🐺🎮
Chatbot interativo para fãs do time FURIA no CS:GO e CS2, trazendo notícias, rankings, torneios e informações atualizadas.

## 🚀 Funcionalidades
- 📋 Menu principal e submenus interativos.
- 📰 Geração de notícias fictícias sobre o time FURIA usando IA (Google Gemini).
- 🏆 Ranking Mundial e Brasileiro de equipes de CS2, e posição atual da FURIA.
- 🏅 Informações sobre torneios atuais, resultados recentes e campeonatos futuros.
- 💬 Links para comunidades e fóruns de CS:GO/CS2.
- 📲 Contato direto com a equipe FURIA (WhatsApp e Instagram).
- ✅ Resposta automática para mensagens inválidas, redirecionando ao menu principal.

## 🛠️ Comandos Disponíveis
- `/start` – Inicia o bot e apresenta o menu principal.
- `/restart` – Reinicia a conversa com o bot.
- `/info` – Apresenta informações sobre o bot.
- `/sair` – Finaliza a sessão de conversa.

## 📦 Tecnologias Utilizadas
- [Python 3.13.3](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/) (v20+)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [aiohttp](https://docs.aiohttp.org/)
- [Google Gemini API](https://ai.google.dev/)

## 🛠️ Como usar
1. Clone este repositório:
git clone https://github.com/VitorZanela/chatbotCS.git
2. Instale as dependencias:
pip install -r requirements.txt
3. cria um doc .env para cadastro do seu Token, no seguinte formato:
    - TOKEN=123456789:seu_token_aqui
    - GEMINI_API_KEY=sua_api_key_gemini
4. Configure o seus Tokens
# 🔑 Configurando o Token do Bot (Telegram)
- Crie seu bot com o [BotFather](https://t.me/botfather) no Telegram:
- Busque por @BotFather  
- Inicie uma conversa com o comando `/newbot`
- Siga as instruções e ao final você receberá um `TOKEN`
- Substitua o valor da variável: TOKEN=token recebido pelo botfather na pasta .env
# 🔑 Configurando o Token do Bot (Gemini)
- Acesse o site do [Google AI Studio](https://aistudio.google.com/welcome)
- Clique em Read API Docs
- Faça login com a sua conta google
- Após logado, clicar em "Gerar uma chave API Gemini"
- Clicar entao em "Get API Key"
- Depois clicar em  "Criar chave de API"
- Copie o Token gerado e substitua na variavel: GEMINI_API_KEY=sua_api_key_gemini na pasta .env

 ## ❗ Informações importantes
- Todas as notícias geradas são fictícias, criadas via inteligência artificial (IA) e simulam o estilo jornalístico de eSports.
- As informações sobre rankings, torneios e fóruns possuem links externos para fontes reais.
- Caso as APIs estejam indisponíveis, mensagens de erro serão exibidas no bot.

