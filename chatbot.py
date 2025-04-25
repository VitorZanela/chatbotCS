from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("TOKEN")

TOKEN = ''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Notícias", callback_data='noticias')],
        [InlineKeyboardButton("Dicas", callback_data='dicas')],
        [InlineKeyboardButton("Campeonatos", callback_data='campeonatos')],
        [InlineKeyboardButton("Curiosidades", callback_data='curiosidades')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Fala jogador! O que você quer saber sobre CS?", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    resposta = {
        'noticias': " Últimas notícias: Novo patch do CS2 anunciado!",
        'dicas': " Dica: Use o som ao seu favor. Escute os passos e saiba a posição dos inimigos!",
        'campeonatos': " Próximo major: IEM Cologne - Julho 2025",
        'curiosidades': " Curiosidade: O mapa Dust2 existe desde 2001!"
    }

    await query.edit_message_text(text=resposta.get(query.data, "Opção inválida."))


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()