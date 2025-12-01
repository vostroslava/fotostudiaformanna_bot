"""
Обработчик сценария "Кадр 'я — организатор'"
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import Callbacks, States
from messages.texts import ORGANIZER_START, get_organizer_compliment, NEED_PHOTO_MESSAGE


async def organizer_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало сценария организатора"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(ORGANIZER_START)
    
    return States.ORGANIZER_PHOTO


async def organizer_photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено фото организатора"""
    if not update.message.photo:
        await update.message.reply_text(NEED_PHOTO_MESSAGE)
        return States.ORGANIZER_PHOTO
    
    # Отправляем комплимент
    compliment = get_organizer_compliment()
    await update.message.reply_text(compliment)
    
    # Кнопка возврата в меню
    keyboard = [[InlineKeyboardButton("Ещё один режим", callback_data=Callbacks.MAIN_MENU)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Попробуешь другой сценарий?",
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
