"""
Обработчик сценария "Просто комплимент"
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import Callbacks, States
from messages.texts import COMPLIMENT_START, get_simple_compliment, NEED_PHOTO_MESSAGE


async def compliment_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало сценария комплимента"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(COMPLIMENT_START)
    
    return States.COMPLIMENT_PHOTO


async def compliment_photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено фото для комплимента"""
    if not update.message.photo:
        await update.message.reply_text(NEED_PHOTO_MESSAGE)
        return States.COMPLIMENT_PHOTO
    
    # Отправляем комплимент
    compliment = get_simple_compliment()
    await update.message.reply_text(compliment)
    
    # Кнопка возврата в меню
    keyboard = [[InlineKeyboardButton("В главное меню", callback_data=Callbacks.MAIN_MENU)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Ещё разок?",
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
