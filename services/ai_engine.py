"""
AI Engine - تحليل الشارتات باستخدام Gemini
"""

import google.generativeai as genai
from PIL import Image
import os
import logging
from services.config import GEMINI_API_KEY

# تكوين التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تكوين Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✅ Gemini API configured")
except Exception as e:
    logger.error(f"❌ Gemini config error: {str(e)}")

def analyze_chart_with_gemini(image_path):
    """تحليل صورة الشارت باستخدام Gemini Vision"""
    try:
        logger.info(f"📊 Analyzing: {image_path}")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(image_path)
        
        prompt = """
        📊 تحليل فني لشارت الذهب (XAUUSD) باستخدام SMC و ICT
        
        حلل هذه الشارت وأعطني:
        
        1. الاتجاه العام (صاعد/هابط/متماسك)
        2. أفضل Order Block (OB) مع المستوى السعري
        3. أفضل Fair Value Gap (FVG) مع المستوى
        4. مناطق السيولة (Liquidity Pools)
        5. سيناريو التداول المقترح:
           - نقطة الدخول (Entry)
           - وقف الخسارة (SL)
           - جني الأرباح (TP1 & TP2)
        6. ملخص بالدارجة المغربية
        
        استخدم لغة واضحة مع رموز تعبيرية.
        """
        
        response = model.generate_content([prompt, img])
        logger.info("✅ Analysis complete")
        
        # إضافة تذييل
        footer = f"""
        ---
        🤖 تحليل بواسطة Gold AI - {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
        ⚠️ للتوعية فقط - استثمر بمسؤولية
        """
        
        return response.text + footer
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise Exception(f"خطأ في Gemini: {str(e)}")