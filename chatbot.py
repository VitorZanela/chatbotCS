from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters, MessageHandler
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def mensagem_invalida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Menu Principal":
        await mostrar_menu_principal(update, context)
    elif text == "🚪 Sair":
        await sair(update, context)
    elif text == "Reiniciar":
        await start(update, context)
    else:
        await update.message.reply_text(
            "🚫 *Mensagem não reconhecida*🚫\n\n"
            "Use o menu para acessar as opções de\n*Início* e *Informações sobre o bot*.\n"
            "Ou, se preferir, digite /start para iniciar",
            parse_mode="Markdown",
            reply_markup=gerar_menu()
        )

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
            InlineKeyboardButton("Dicas", callback_data='dicas')
        ],
        [
            InlineKeyboardButton("Campeonatos", callback_data='campeonatos'),
            InlineKeyboardButton("Curiosidades", callback_data='curiosidades')
        ],
        [InlineKeyboardButton("Contatos FURIA", callback_data='contato')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Escolha uma opção no menu abaixo:", 
        reply_markup=reply_markup
    )

def gerar_menu():
    keyboard = [
        ["📋 Menu Principal"],
        ["Reiniciar", "🚪 Sair"],
        ["Mais info sobre o Bot"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    resposta = {
        'noticias': " Últimas notícias: Novo patch do CS2 anunciado!",
        'dicas': " Dica: Use o som ao seu favor. Escute os passos e saiba a posição dos inimigos!",
        'campeonatos': " Próximo major: IEM Cologne - Julho 2025",
        'curiosidades': " Curiosidade: O mapa Dust2 existe desde 2001!",
        'contato': "- Entre em contato com a FURIA pelo WhatsApp: [Contato Inteligente FURIA](https://wa.me/5511993404466)\n\n- Ou fique à vontade para seguir a FURIA no [Instagram](https://www.instagram.com/furiagg)"
    }

    await query.edit_message_text(
    text=resposta.get(query.data, "Opção inválida."),
    parse_mode="Markdown",
    disable_web_page_preview=True
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