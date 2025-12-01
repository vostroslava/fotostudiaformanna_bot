"""
Обработчик сценария "Портрет для себя"
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import Callbacks, States
from messages.texts import (
    PORTRAIT_START, PORTRAIT_TIPS, 
    get_portrait_compliment, NEED_PHOTO_MESSAGE
)


async def portrait_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало сценария портрета"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Нежный", callback_data=Callbacks.PORTRAIT_GENTLE)],
        [InlineKeyboardButton("С дерзинкой", callback_data=Callbacks.PORTRAIT_BOLD)],
        [InlineKeyboardButton("Деловой", callback_data=Callbacks.PORTRAIT_BUSINESS)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        PORTRAIT_START,
        reply_markup=reply_markup
    )
    
    return States.PORTRAIT_TYPE


async def portrait_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь выбрал тип портрета"""
    query = update.callback_query
    await query.answer()
    
    # Определяем тип портрета
    portrait_type_map = {
        Callbacks.PORTRAIT_GENTLE: 'gentle',
        Callbacks.PORTRAIT_BOLD: 'bold',
        Callbacks.PORTRAIT_BUSINESS: 'business'
    }
    
    portrait_type = portrait_type_map.get(query.data)
    context.user_data['portrait_type'] = portrait_type
    
    # Отправляем подсказки
    await query.edit_message_text(PORTRAIT_TIPS[portrait_type])
    
    return States.PORTRAIT_PHOTO


async def portrait_photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено фото для портрета"""
    if not update.message.photo:
        await update.message.reply_text(NEED_PHOTO_MESSAGE)
        return States.PORTRAIT_PHOTO
    
    portrait_type = context.user_data.get('portrait_type', 'gentle')
    
    # Отправляем комплимент
    compliment = get_portrait_compliment(portrait_type)
    await update.message.reply_text(compliment)
    
    # Кнопка возврата в меню
    keyboard = [[InlineKeyboardButton("В главное меню", callback_data=Callbacks.MAIN_MENU)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Хочешь попробовать что-то ещё?",
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
