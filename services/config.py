import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

APP_NAME = "Gold AI"
APP_VERSION = "2.0.0"
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

GOLD_SYMBOL = "XAUUSD"
GOLD_CURRENCY = "USD"