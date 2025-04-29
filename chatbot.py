from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters, MessageHandler
from dotenv import load_dotenv
import aiohttp

import os

from yarl import Query

load_dotenv()
TOKEN = os.environ.get("TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def gerar_menu():
    keyboard = [
        ["📋 Menu Principal"],
        ["♻️ Reiniciar", "ℹ️ Info sobre o Bot"],
        ["🚪 Sair"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def mensagem_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Menu Principal":
        await mostrar_menu_principal(update, context)
    elif text == "🚪 Sair":
        await sair(update, context)
    elif text == "♻️ Reiniciar":
        await start(update, context)
    elif text == "ℹ️ Info sobre o Bot":
        info_text = (
        "ℹ️ *Informações sobre o Bot* ℹ️\n\n"
        "Este bot fornece notícias, rankings, torneios e curiosidades sobre o time de CS:GO da FURIA! 🐺\n\n\n"
        "_Criado e desenvolvido por Vitor Zanela_\n"
        "*OBS:* _Todas as noticias sobre a FURIA e sobre o Time da FURIA são geradas por IA e são fictícias_"
        )
        info_keyboard = [
            [InlineKeyboardButton("📋 Menu Principal", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(info_keyboard)
        await update.message.reply_text(
        text=info_text,
        parse_mode="Markdown",
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            "🚫 *Mensagem não reconhecida!* 🚫\n\n"
            "Não se preocupe 🙌\n"
            "Você será redirecionado para o *menu principal*.",
            parse_mode="Markdown"
        )
        await mostrar_menu_principal(update, context)

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
            [InlineKeyboardButton("🔙 Voltar", callback_data='voltar_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(ranking_keyboard)
        await query.edit_message_text(text="🏆 Escolha o tipo de ranking:", reply_markup=reply_markup)

    elif query.data == 'torneios':

        torneios_keyboard = [
            [
                InlineKeyboardButton("Torneios Atuais", callback_data='torneios_atuais'),
                InlineKeyboardButton("Resultados Recentes", callback_data='resultados_recentes')
            ],
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
        voltar_keyboard = [
        [InlineKeyboardButton("🔙 Voltar para Noticias", callback_data='noticias')]
    ]
    reply_markup = InlineKeyboardMarkup(voltar_keyboard)

    if query.data in ['ultimas_noticias', 'noticias_furia']:

        await query.edit_message_text(
            text="🔄 Buscando notícias... aguarde!",
            parse_mode="Markdown"
        )

        if query.data == 'ultimas_noticias':
            texto = await buscar_noticias_gemini("Últimas notícias da FURIA E-sports")
        else:
            texto = await buscar_noticias_gemini("Últimas notícias do time de CS da FURIA")

        await query.edit_message_text(
            text=texto,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

    else:
        if query.data == 'atualizacoes_cs2':
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar para Notícias", callback_data='noticias')]
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)

            texto = "🛠️ Atualizações no CS2\n\n" \
                    "• Atualizações disponíveis: [Acesse aqui](https://draft5.gg/cs-atualizacoes)\n"
            
        elif query.data == 'ranking_mundial':
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar para Ranking", callback_data='ranking')]
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)
            texto = (
                    "🌎 Ranking Mundial - CS2\n\n" 
                    "• Veja o ranking mundial atualizado do dia *21/04/2025*: [Clique aqui para conferir](https://www.hltv.org/ranking/teams/2025/april/21)\n" 
                    "• Até esssa atualização a equipe do FURIA esta na 16ª Posição\n\n" 
                    "💬 Dica:\n" 
                    "• Dá pra mudar o idioma do site para *português!*\n" 
                    "• Também é possível filtrar para ver rankings de outras datas!"
                )
            
        elif query.data == 'ranking_brasileiro':
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar para Ranking", callback_data='ranking')]
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)
            texto = (
                    "🌎 Ranking Mundial - CS2\n\n" 
                    "• Veja o ranking Brasileiro atualizado do dia *21/04/2025*: [Clique aqui para conferir](https://www.hltv.org/ranking/teams/2025/april/21/country/Brazil)\n" 
                    "• Até esssa atualização a equipe do FURIA esta na 1ª Posição\n\n" 
                    "💬 Dica:\n" 
                    "• Dá pra mudar o idioma do site para *português!*\n" 
                    "• Também é possível filtrar para ver rankings de outras datas!"
                )
        elif query.data == 'torneios_atuais':
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar para Torneios", callback_data='torneios')]
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)
            texto = (
                    "🏆 *Torneios Recentes e Atuais da FURIA*\n\n"
                    "- Confira os campeonatos em que a FURIA está participando e os resultados mais recentes! 🔥\n\n"
                    "👉 [Clique aqui para acessar](https://draft5.gg/equipe/330-FURIA/campeonatos)"
                )
        elif query.data == 'resultados_recentes':
            voltar_keyboard = [
                [InlineKeyboardButton("🔙 Voltar para Torneios", callback_data='torneios')]
            ]
            reply_markup = InlineKeyboardMarkup(voltar_keyboard)
            texto = (
                    "✅ *Últimos Resultados da FURIA*\n\n"
                    "- Veja os placares e confrontos mais recentes do time! 🐺🔥\n\n"
                    "👉 [Clique aqui para acessar](https://draft5.gg/equipe/330-FURIA/resultados)"
                )
        else:
            texto = "⚠️ Opção inválida."

        await query.edit_message_text(
            text=texto,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = (
        "ℹ️ *Informações sobre o Bot* ℹ️\n\n"
        "Este bot fornece notícias, rankings, torneios e curiosidades sobre o time de CS:GO da FURIA! 🐺\n\n\n"
        "_Criado e desenvolvido por Vitor Zanela_\n"
        "*OBS:* _Informações de noticias ficcticia_"
    )
    info_keyboard = [
        [InlineKeyboardButton("📋 Menu Principal", callback_data='voltar_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(info_keyboard)
    await update.message.reply_text(
        text=info_text,
        parse_mode="Markdown",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def buscar_noticias_gemini(tema):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json",
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
                        Você é um assistente especializado em notícias de eSports, focado em Counter-Strike (CS2) e no time FURIA.

                        - Gere as 3 notícias mais recentes sobre o tema '{tema}'.
                        - Cada notícia deve ter:
                            • Um título impactante (no estilo de portais como HLTV.org, Draft5.gg).
                            • Um link fictício para simular a notícia (exemplo: https://noticiascs.com/furia-titulo).
                        - As notícias devem ser em português (Brasil).
                        - Caso não existam notícias reais, crie manchetes plausíveis e realistas.
                        - Não repita temas entre as notícias.
                        - Não inclua mensagens auxiliares nem explicações extras.

                        Responda no seguinte formato:
                        📰 *Título da notícia*
                        [Leia mais aqui](link)

                        Separe cada notícia com uma linha em branco.
                        """
                    }
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            if response.status != 200:
                return "⚠️ Erro ao buscar notícias. Tente novamente mais tarde."
            try:
                resposta = await response.json()
                texto = resposta["candidates"][0]["content"]["parts"][0]["text"]
                return texto
            except Exception as e:
                return "⚠️ Não consegui interpretar as notícias. Tente novamente."

async def set_menu(app):
    commands = [
        BotCommand(command="start", description="Iniciar o bot"),
        BotCommand(command="restart", description="Reiniciar o bot"),
        BotCommand(command="info", description="Mais informações sobre o bot"),
        BotCommand(command="sair", description="Finalizar sessão com o bot"),
    ]
    await app.bot.set_my_commands(commands)

async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sessão encerrada! 👋",
        reply_markup=gerar_menu()
    )


app = Application.builder().token(TOKEN).post_init(set_menu).build()
app.add_handler(CommandHandler(["start", "restart"], start))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("sair", sair))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_menu))
app.run_polling()
