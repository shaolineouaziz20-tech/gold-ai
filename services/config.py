"""
ملف الإعدادات العامة للمشروع
"""

import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# ==================== Gemini API ====================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

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
        'gold_symbol': GOLD_SYMBOL,
    }