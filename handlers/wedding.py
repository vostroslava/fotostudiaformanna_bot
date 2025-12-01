"""
Обработчик сценария "Свадебная мечта"
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import Callbacks, States
from messages.texts import (
    WEDDING_START, WEDDING_TIPS,
    get_wedding_compliment, NEED_PHOTO_MESSAGE
)


async def wedding_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало свадебного сценария"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Камерная и ламповая", callback_data=Callbacks.WEDDING_INTIMATE)],
        [InlineKeyboardButton("Большая вечеринка", callback_data=Callbacks.WEDDING_BIG)],
        [InlineKeyboardButton("Что-то между", callback_data=Callbacks.WEDDING_MIXED)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        WEDDING_START,
        reply_markup=reply_markup
    )
    
    return States.WEDDING_TYPE


async def wedding_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пользователь выбрал тип свадьбы"""
    query = update.callback_query
    await query.answer()
    
    # Определяем тип свадьбы
    wedding_type_map = {
        Callbacks.WEDDING_INTIMATE: 'intimate',
        Callbacks.WEDDING_BIG: 'big',
        Callbacks.WEDDING_MIXED: 'mixed'
    }
    
    wedding_type = wedding_type_map.get(query.data)
    context.user_data['wedding_type'] = wedding_type
    
    # Отправляем подсказки
    await query.edit_message_text(WEDDING_TIPS[wedding_type])
    
    return States.WEDDING_PHOTO


async def wedding_photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получено свадебное фото"""
    if not update.message.photo:
        await update.message.reply_text(NEED_PHOTO_MESSAGE)
        return States.WEDDING_PHOTO
    
    # Отправляем комплимент
    compliment = get_wedding_compliment()
    await update.message.reply_text(compliment)
    
    # Добавляем мягкую фразу поддержки
    await update.message.reply_text(
        "Твоей будущей студии и свадьбам мир точно не избежит ✨"
    )
    
    # Кнопка возврата в меню
    keyboard = [[InlineKeyboardButton("В главное меню", callback_data=Callbacks.MAIN_MENU)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Что попробуем ещё?",
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END
