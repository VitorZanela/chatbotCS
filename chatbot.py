from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, filters, MessageHandler
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

async def mensagem_invalida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚫 *Mensagem não reconhecida*🚫\n\n"
        "Use o menu para acessar as opções de *Início* e *Informações do Bot*.\n"
        "Ou, se preferir, digite /start para iniciar",
        parse_mode="Markdown"
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

    user_first_name = update.effective_user.first_name  # pega o primeiro nome do usuário

    welcome_message = (f"Fala {user_first_name}! 👋 Seja muito bem-vindo!\nO que você quer saber sobre o time de CS da FURIA?")

    keyboard = [
        [
            InlineKeyboardButton("Notícias", callback_data='noticias'),
            InlineKeyboardButton("Dicas", callback_data='dicas')
        ],
        [
            InlineKeyboardButton("Campeonatos", callback_data='campeonatos'),
            InlineKeyboardButton("Curiosidades", callback_data='curiosidades')
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    resposta = {
        'noticias': " Últimas notícias: Novo patch do CS2 anunciado!",
        'dicas': " Dica: Use o som ao seu favor. Escute os passos e saiba a posição dos inimigos!",
        'campeonatos': " Próximo major: IEM Cologne - Julho 2025",
        'curiosidades': " Curiosidade: O mapa Dust2 existe desde 2001!"
    }

async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sessão encerrada! 👋",
)


app = Application.builder().token(TOKEN).post_init(set_menu).build()
app.add_handler(CommandHandler(["start", "restart"], start))
app.add_handler(CommandHandler("sair", sair))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_invalida))
app.run_polling()