import google.generativeai as genai
from PIL import Image
import os
import logging
from services.config import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

def analyze_chart_with_gemini(image_path):
    try:
        logger.info(f"📊 Analyzing: {image_path}")
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(image_path)
        
        prompt = """
        📊 **تحليل فني لشارت الذهب (XAUUSD) باستخدام SMC و ICT**
        
        أنت محلل فني خبير في أسواق المال، متخصص في Smart Money Concepts و ICT.
        حلل هذه الشارت بدقة وأعطني التحليل التالي:
        
        1. **الاتجاه العام**: صاعد/هابط/متماسك مع الأسباب
        2. **أفضل منطقة Order Block (OB)**: المستوى السعري + النوع + القوة
        3. **أفضل منطقة Fair Value Gap (FVG)**: المستوى السعري + النوع
        4. **مناطق السيولة**: أقرب High/Low
        5. **سيناريو التداول المقترح**: دخول + خروج + وقف خسارة + R:R
        6. **ملخص بالدارجة المغربية**
        
        استخدم لغة واضحة مع رموز تعبيرية.
        """
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        raise Exception(f"خطأ في Gemini: {str(e)}")