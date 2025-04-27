from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters, MessageHandler
from dotenv import load_dotenv

import requests
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")
API_KEY_NEWS = os.environ.get("API_KEY_NEWS")  # <<< Adicione sua API Key no .env também

def buscar_noticias_cs():
    url = f"https://gnews.io/api/v4/search?q=furia%20esports&lang=pt&token={API_KEY_NEWS}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "⚠️ Erro ao buscar notícias. Tente novamente mais tarde."
    
    dados = response.json()
    artigos = dados.get("articles", [])
    
    if not artigos:
        return "Nenhuma notícia encontrada no momento. 🔍"
    
    mensagens = []
    for artigo in artigos[:5]:
        titulo = artigo["title"]
        link = artigo["url"]
        mensagens.append(f"📰 *{titulo}*\n[Leia mais aqui]({link})")
    
    return "\n\n".join(mensagens)

def buscar_noticias_furiacs():
    url = f"https://gnews.io/api/v4/search?q=furia%20counter%20strike&lang=pt&token={API_KEY_NEWS}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "⚠️ Erro ao buscar notícias. Tente novamente mais tarde."
    
    dados = response.json()
    artigos = dados.get("articles", [])
    
    if not artigos:
        return "Nenhuma notícia encontrada no momento. 🔍"
    
    mensagens = []
    for artigo in artigos[:5]:  # Pega as 5 notícias mais recentes
        titulo = artigo["title"]
        link = artigo["url"]
        mensagens.append(f"📰 *{titulo}*\n[Leia mais aqui]({link})")
    
    return "\n\n".join(mensagens)

async def mensagem_invalida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Menu Principal":
        await mostrar_menu_principal(update, context)
    elif text == "🚪 Sair":
        await sair(update, context)
    elif text == "♻️ Reiniciar":
        await start(update, context)
    elif text == "ℹ️ Mais info sobre o Bot":
        await update.message.reply_text(
            "ℹ️ *Informações sobre o Bot* ℹ️\n\n"
            "Este bot fornece notícias, rankings, torneios e curiosidades sobre o time de CS:GO da FURIA! 🐺",
            parse_mode="Markdown",
            reply_markup=gerar_menu()
        )
    else:
        await update.message.reply_text(
            "🚫 *Mensagem não reconhecida!* 🚫\n\n"
            "Não se preocupe 🙌\n"
            "Você será redirecionado para o *menu principal*.",
            parse_mode="Markdown"
        )
        await mostrar_menu_principal(update, context)

async def set_menu(app):
    commands = [
        BotCommand(command="start", description="Iniciar o bot"),
        BotCommand(command="restart", description="Reiniciar o bot"),
        BotCommand(command="info", description="Mais informações sobre o bot"),
        BotCommand(command="sair", description="Finalizar sessão com o bot"),
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name

    welcome_message = (f"Fala {user_first_name}! 👋 Seja muito bem-vindo(a)!\nO que você quer saber sobre o time de CS da FURIA?")

    await update.message.reply_text(welcome_message, reply_markup=gerar_menu())
    await mostrar_menu_principal(update, context)

async def mostrar_menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Notícias", callback_data='noticias'),
            InlineKeyboardButton("Ranking", callback_data='ranking')
        ],
        [
            InlineKeyboardButton("Torneios", callback_data='torneios'),
            InlineKeyboardButton("Forúm CS:GO", callback_data='forum')
        ],
        [InlineKeyboardButton("Contatos FURIA", callback_data='contato')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Escolha uma opção no menu abaixo:",
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "Escolha uma opção no menu abaixo:",
            reply_markup=reply_markup
        )

def gerar_menu():
    keyboard = [
        ["📋 Menu Principal"],
        ["♻️ Reiniciar", "🚪 Sair"],
        ["ℹ️ Mais info sobre o Bot"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'noticias':

        noticias_keyboard = [
            [
                InlineKeyboardButton("Sobre a FURIA", callback_data='ultimas_noticias'),
                InlineKeyboardButton("Time de CS da FURIA", callback_data='noticias_furia'),   
            ],
            [InlineKeyboardButton("Atualizações do CS2", callback_data='atualizacoes_cs2')],
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(noticias_keyboard)
        await query.edit_message_text(text="📰 Escolha uma categoria de notícias:", reply_markup=reply_markup)

    elif query.data == 'ranking':

        ranking_keyboard = [
            [
                InlineKeyboardButton("Ranking Mundial", callback_data='ranking_mundial'),
                InlineKeyboardButton("Ranking Brasileiro", callback_data='ranking_brasileiro')
            ],
            [InlineKeyboardButton("Posição da FURIA", callback_data='posicao_furia')],
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(ranking_keyboard)
        await query.edit_message_text(text="🏆 Escolha o tipo de ranking:", reply_markup=reply_markup)

    elif query.data == 'torneios':

        torneios_keyboard = [
            [
                InlineKeyboardButton("Torneios Atuais", callback_data='torneios_atuais'),
                InlineKeyboardButton("Próximos Torneios", callback_data='proximos_torneios')
            ],
            [InlineKeyboardButton("Resultados Recentes", callback_data='resultados_recentes')],
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(torneios_keyboard)
        await query.edit_message_text(text="🏅 Informações sobre os torneios:", reply_markup=reply_markup)

    elif query.data == 'forum':
        forum_text = (
        "💬 Participe de comunidades de CS!\n\n"
        "- Fórum Reddit CS:GO: [Acesse aqui](https://www.reddit.com/r/GlobalOffensive/)\n"
        "- Discord Draft5: [Acesse aqui](https://discord.gg/draft5)"
        )
        forum_keyboard = [
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(forum_keyboard)
        await query.edit_message_text(
            text=forum_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    elif query.data == 'contato':
        contato_text = (
        "💬 Entre em contato com a FURIA!\n\n"
        "- WhatsApp: [Contato Inteligente FURIA](https://wa.me/5511993404466)\n"
        "- Instagram: [Acesse aqui](https://www.instagram.com/furiagg)"
        )
        contato_keyboard = [
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(contato_keyboard)
        await query.edit_message_text(
            text=contato_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    elif query.data == 'voltar_menu':

        await mostrar_menu_principal(update, context)

    else:
        if query.data in ['ultimas_noticias', 'noticias_furia', 'atualizacoes_cs2', 
                        'ranking_mundial', 'ranking_brasileiro', 'posicao_furia',
                        'torneios_atuais', 'proximos_torneios', 'resultados_recentes']:
            
            resposta = {
                'ultimas_noticias': buscar_noticias_cs(),
                'noticias_furia': buscar_noticias_furiacs(),
                'atualizacoes_cs2': "🛠️ Atualizações CS2: Novo mapa 'Inferno' reformulado!",
                'ranking_mundial': "🌎 Ranking Mundial: 1º - Vitality | 2º - G2 | 3º - FaZe",
                'ranking_brasileiro': "🇧🇷 Ranking Brasileiro: 1º - FURIA | 2º - Imperial | 3º - MIBR",
                'posicao_furia': "📈 A FURIA está atualmente na 9ª posição mundial!",
                'torneios_atuais': "🏅 Torneios em andamento: ESL Pro League - Temporada 20",
                'proximos_torneios': "🗓️ Próximos Torneios: Blast Premier Fall 2025",
                'resultados_recentes': "✅ Resultados recentes: Vitória da FURIA contra a NAVI por 2-0"
            }
            
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar", callback_data='noticias')]  # Volta para o menu de notícias
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)

            await query.edit_message_text(
                text=resposta.get(query.data, "Opção inválida."),
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        
        else:
            await query.edit_message_text(
                text="Opção inválida.",
                parse_mode="Markdown"
            )


async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sessão encerrada! 👋",
        reply_markup=gerar_menu()
    )


app = Application.builder().token(TOKEN).post_init(set_menu).build()
app.add_handler(CommandHandler(["start", "restart"], start))
app.add_handler(CommandHandler("sair", sair))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_invalida))
app.run_polling()
