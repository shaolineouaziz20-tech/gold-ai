"""
AI Engine - تحليل الشارتات باستخدام الذكاء الاصطناعي Gemini
"""

import google.generativeai as genai
from PIL import Image
import os
import logging
from services.config import GEMINI_API_KEY

# تكوين التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تكوين Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✅ Gemini API configured successfully")
except Exception as e:
    logger.error(f"❌ Failed to configure Gemini API: {str(e)}")

def analyze_chart_with_gemini(image_path):
    """
    تحليل صورة الشارت باستخدام Google Gemini Vision API
    
    Args:
        image_path (str): مسار الصورة المراد تحليلها
        
    Returns:
        str: نتيجة التحليل مع التوصيات
    """
    try:
        logger.info(f"📊 Starting analysis of: {image_path}")
        
        # اختيار النموذج
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # قراءة الصورة
        img = Image.open(image_path)
        logger.info(f"📸 Image loaded: {img.size} pixels")
        
        # الـ Prompt المحسن للتحليل SMC / ICT
        prompt = """
        📊 **تحليل فني متقدم لشارت الذهب (XAUUSD) باستخدام Smart Money Concepts (SMC) و ICT**
        
        أنت محلل فني خبير في أسواق المال، متخصص في تحليل Smart Money Concepts و Inner Circle Trader.
        حلل هذه الشارت بدقة وأعطني التحليل التالي:
        
        ---
        
        📈 **1. الاتجاه العام (Market Structure)**
        - هل السوق صاعد (Bullish) أم هابط (Bearish) أم متماسك (Range)؟
        - اذكر الأسباب من الشارت (الهاي واللو، الترند، تشكيل القمم والقيعان)
        
        🎯 **2. مناطق السيولة (Liquidity Pools)**
        - أعلى سعر (High) وأقل سعر (Low) واضحين على الشارت
        - نقاط جذب السيولة (Liquidity Sweeps) إن وجدت
        
        🧱 **3. أفضل منطقة Order Block (OB)**
        - المستوى السعري المحدد
        - نوعه: Bullish OB (شراء) أم Bearish OB (بيع)
        - قوته: ضعيف / متوسط / قوي
        - سبب اختيارك لهذه المنطقة تحديداً
        
        🕳️ **4. أفضل منطقة Fair Value Gap (FVG)**
        - المستوى السعري المحدد
        - نوعه: Bullish FVG أم Bearish FVG
        - هل تم اختباره من قبل؟ إن كانت الإجابة نعم، كيف كان رد فعل السعر؟
        
        🔄 **5. نقاط الانعكاس المتوقعة (POI - Points of Interest)**
        - مناطق تقاطع الـ OB مع الـ FVG
        - مناطق الانعكاس المحتملة
        
        📊 **6. سيناريو التداول المقترح (Trading Plan)**
        - نقطة الدخول (Entry Price): مستوى محدد
        - وقف الخسارة (Stop Loss): مستوى محدد مع السبب
        - جني الأرباح الأول (TP1): مستوى محدد
        - جني الأرباح الثاني (TP2): مستوى محدد
        - نسبة المخاطرة/المكافأة (Risk/Reward Ratio)
        
        🗣️ **7. ملخص بالدارجة المغربية للمتداول**
        - اشرح الوضع ببساطة ووضوح
        - أعط نصيحة عملية للمتداول
        
        ---
        
        ⚠️ **ملاحظة مهمة:** هذا التحليل هو لأغراض تعليمية فقط وليس توصية بالشراء أو البيع. أنت مسؤول عن قراراتك الاستثمارية.
        
        استخدم لغة واضحة ومباشرة، ورتب المعلومات بشكل منظم مع استخدام الرموز التعبيرية.
        """
        
        # إرسال الطلب لـ Gemini
        logger.info("🔄 Sending request to Gemini API...")
        response = model.generate_content([prompt, img])
        
        # تنظيف النتيجة
        result = response.text
        logger.info("✅ Analysis completed successfully")
        
        # إضافة تذييل
        footer = """
        
        ---
        🤖 **تحليل بواسطة Gold AI باستخدام Google Gemini**
        ⚠️ للتوعية فقط - استثمر بمسؤولية
        """
        
        return result + footer
        
    except Exception as e:
        error_msg = f"❌ خطأ في Gemini API: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)