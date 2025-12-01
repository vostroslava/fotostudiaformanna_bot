"""
Конфигурация бота и константы
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Состояния для ConversationHandler
class States:
    # Портрет для себя
    PORTRAIT_TYPE = 0
    PORTRAIT_PHOTO = 1
    
    # Кадр организатор
    ORGANIZER_PHOTO = 2
    
    # Свадебная мечта
    WEDDING_TYPE = 3
    WEDDING_PHOTO = 4
    
    # Просто комплимент
    COMPLIMENT_PHOTO = 5

# Callback data для кнопок
class Callbacks:
    # Главное меню
    PORTRAIT = "portrait"
    ORGANIZER = "organizer"
    WEDDING = "wedding"
    COMPLIMENT = "compliment"
    MAIN_MENU = "main_menu"
    
    # Типы портретов
    PORTRAIT_GENTLE = "portrait_gentle"
    PORTRAIT_BOLD = "portrait_bold"
    PORTRAIT_BUSINESS = "portrait_business"
    
    # Типы свадеб
    WEDDING_INTIMATE = "wedding_intimate"
    WEDDING_BIG = "wedding_big"
    WEDDING_MIXED = "wedding_mixed"
