#!/usr/bin/env python3
"""
Telegram Bot: Персональная фотостудия (WebApp Launcher)
Романтический подарок от Славы
"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler

from config import TELEGRAM_BOT_TOKEN
from handlers.start import start_command

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
    
    # Регистрируем только команду /start
    application.add_handler(CommandHandler("start", start_command))
    
    # Запускаем бота
    logger.info("Бот запущен! 💫 (WebApp Mode)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
