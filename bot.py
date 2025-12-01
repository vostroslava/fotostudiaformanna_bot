#!/usr/bin/env python3
"""
Telegram Bot: Персональная фотостудия
Романтический подарок от Славы

Маленькая виртуальная фотостудия для мини-съёмок и комплиментов
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import TELEGRAM_BOT_TOKEN, States, Callbacks
from handlers.start import start_command, show_main_menu
from handlers.portrait import portrait_start, portrait_type_selected, portrait_photo_received
from handlers.organizer import organizer_start, organizer_photo_received
from handlers.wedding import wedding_start, wedding_type_selected, wedding_photo_received
from handlers.compliment import compliment_start, compliment_photo_received

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Запуск бота"""
    
    # Проверка токена
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не найден! Создайте .env файл с токеном.")
        return
    
    # Создаём приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # ConversationHandler для всех сценариев
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(portrait_start, pattern=f"^{Callbacks.PORTRAIT}$"),
            CallbackQueryHandler(organizer_start, pattern=f"^{Callbacks.ORGANIZER}$"),
            CallbackQueryHandler(wedding_start, pattern=f"^{Callbacks.WEDDING}$"),
            CallbackQueryHandler(compliment_start, pattern=f"^{Callbacks.COMPLIMENT}$"),
        ],
        states={
            States.PORTRAIT_TYPE: [
                CallbackQueryHandler(
                    portrait_type_selected,
                    pattern=f"^({Callbacks.PORTRAIT_GENTLE}|{Callbacks.PORTRAIT_BOLD}|{Callbacks.PORTRAIT_BUSINESS})$"
                )
            ],
            States.PORTRAIT_PHOTO: [
                MessageHandler(filters.ALL, portrait_photo_received)
            ],
            States.ORGANIZER_PHOTO: [
                MessageHandler(filters.ALL, organizer_photo_received)
            ],
            States.WEDDING_TYPE: [
                CallbackQueryHandler(
                    wedding_type_selected,
                    pattern=f"^({Callbacks.WEDDING_INTIMATE}|{Callbacks.WEDDING_BIG}|{Callbacks.WEDDING_MIXED})$"
                )
            ],
            States.WEDDING_PHOTO: [
                MessageHandler(filters.ALL, wedding_photo_received)
            ],
            States.COMPLIMENT_PHOTO: [
                MessageHandler(filters.ALL, compliment_photo_received)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(show_main_menu, pattern=f"^{Callbacks.MAIN_MENU}$"),
            CommandHandler("start", start_command)
        ],
        allow_reentry=True,
        per_message=True
    )
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern=f"^{Callbacks.MAIN_MENU}$"))
    
    # Запускаем бота
    logger.info("Бот запущен! 💫")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
