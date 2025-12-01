"""
Обработчик команды /start и главного меню
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import Callbacks
from messages.texts import WELCOME_MESSAGE, MAIN_MENU_TEXT


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Портрет для себя", callback_data=Callbacks.PORTRAIT)],
        [InlineKeyboardButton("Кадр \"я — организатор\"", callback_data=Callbacks.ORGANIZER)],
        [InlineKeyboardButton("Свадебная мечта", callback_data=Callbacks.WEDDING)],
        [InlineKeyboardButton("Просто комплимент", callback_data=Callbacks.COMPLIMENT)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Портрет для себя", callback_data=Callbacks.PORTRAIT)],
        [InlineKeyboardButton("Кадр \"я — организатор\"", callback_data=Callbacks.ORGANIZER)],
        [InlineKeyboardButton("Свадебная мечта", callback_data=Callbacks.WEDDING)],
        [InlineKeyboardButton("Просто комплимент", callback_data=Callbacks.COMPLIMENT)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        MAIN_MENU_TEXT,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
