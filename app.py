import os
import io
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

# imports ديال السيستيم القديم ديالك باش يطيروا الأخطاء ف المجلدات الأخرى
from services.ai_engine import * 
from services.news_fetcher import *

app = Flask(__name__)

# ==========================================
# 1. إعداد الـ Gemini API والـ Key ديالك
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6IHbXcjEcC2hXRGHQmropcrT7neFd0u89js_VAeR3Dk0w"
genai.configure(api_key=GEMINI_API_KEY)


# ==========================================
# 2. الـ Routes (الصفحات ديال الموقع)
# ==========================================

# صفحة الـ Dashboard الرئيسية (ديال الـ Live Price والأخبار)
@app.route('/')
def index():
    # كيرجع يخدم السيستيم القديم ديالك أوتوماتيكياً بلا ما يفركع الـ index.html
    return render_template('index.html')


# صفحة الـ AI Analyse الجديدة (فين غاتحط السكرين شوت)
@app.route('/ai-analyse', methods=['GET', 'POST'])
def ai_analyse():
    if request.method == 'GET':
        return render_template('ai_analyse.html')
    
    if request.method == 'POST':
        if 'chart_img' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
            
        file = request.files['chart_img']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        try:
            # قراءة التصويرة وتحويلها لـ PIL Image باش يفهمها Gemini
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # الـ Prompt الموجه والمثالي للـ SMC والذهب
            prompt = """
            You are an expert Smart Money Concepts (SMC) and ICT trader specializing in XAUUSD (Gold).
            Analyze this chart screenshot and provide a highly professional, detailed technical breakdown in Darija (Moroccan Arabic mixed with trading terms like OB, FVG, Liquidity, Bias, Premium/Discount, Killzones).
            
            Focus heavily on:
            1. High-Probability Order Blocks (OB): Identify the best OB that matches premium/discount zones and has unmitigated liquidity.
            2. Key Fair Value Gaps (FVG) or iFVG: Point out the most important gaps that the market is likely to draw into.
            3. Liquidity & DOL (Draw on Liquidity): Where are the stops sitting? (PDH, PDL, Session Highs/Lows).
            4. Execution Verdict: Based on the trend and high-timeframe context visible, what is the highest probability setup to wait for?
            
            Keep the response structured, sharp, and easy to read using bullet points. Write in Moroccan Darija Arabic script.
            """
            
            # استدعاء الموديل Gemini 1.5 Flash السريع والقوي ف الرؤية
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([prompt, image])
            
            return jsonify({'analysis': response.text})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# ==========================================
# 3. تشغيل السيرفر المحلي (Local)
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)