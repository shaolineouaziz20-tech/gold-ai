"""
ملف الإعدادات العامة للمشروع
"""

import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# ==================== Gemini API ====================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

# ==================== Telegram Bot ====================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# ==================== API Keys ====================
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'YOUR_NEWS_API_KEY_HERE')
FOREX_FACTORY_KEY = os.getenv('FOREX_FACTORY_KEY', 'YOUR_FOREX_FACTORY_KEY_HERE')

# ==================== إعدادات التطبيق ====================
APP_NAME = "Gold AI"
APP_VERSION = "2.0.0"
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ==================== إعدادات الذهب ====================
GOLD_SYMBOL = "XAUUSD"
GOLD_CURRENCY = "USD"

# ==================== إعدادات التحليل ====================
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'gif']

# ==================== إعدادات الجلسات ====================
SESSION_TIMES = {
    'asia': {'open': '00:00', 'close': '09:00'},
    'london': {'open': '08:00', 'close': '17:00'},
    'newyork': {'open': '13:00', 'close': '22:00'}
}

# ==================== إعدادات التداول ====================
MAX_LEVERAGE = 100
MIN_DEPOSIT = 100
DEFAULT_RISK_PERCENT = 2

# ==================== إعدادات البيانات ====================
CACHE_TIMEOUT = 60  # ثواني
PRICE_UPDATE_INTERVAL = 30  # ثواني

def get_config():
    """إرجاع جميع الإعدادات كـ قاموس"""
    return {
        'app_name': APP_NAME,
        'app_version': APP_VERSION,
        'debug': DEBUG,
        'gemini_api_key': GEMINI_API_KEY,
        'telegram_bot_token': TELEGRAM_BOT_TOKEN,
        'telegram_chat_id': TELEGRAM_CHAT_ID,
        'news_api_key': NEWS_API_KEY,
        'gold_symbol': GOLD_SYMBOL,
        'session_times': SESSION_TIMES
    }