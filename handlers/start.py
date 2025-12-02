"""
Обработчик команды /start и главного меню
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler

from messages.texts import WELCOME_MESSAGE


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    # Только одна кнопка - WebApp
    keyboard = [
        [InlineKeyboardButton("📸 Открыть студию", web_app=WebAppInfo(url="https://vostroslava.github.io/fotostudiaformanna_bot/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Если это первый запуск или команда /start
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню (если вдруг вызовется)"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📸 Открыть студию", web_app=WebAppInfo(url="https://vostroslava.github.io/fotostudiaformanna_bot/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Нажми кнопку ниже, чтобы войти в студию 👇",
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
