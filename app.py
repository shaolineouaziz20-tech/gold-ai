from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from services.ai_engine import analyze_chart_with_gemini
from services.gold_price import get_gold_price
from services.forex_factory import get_news
from services.config import GEMINI_API_KEY
from datetime import datetime
import json

app = Flask(__name__)

# إعدادات رفع الصور
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# إنشاء مجلد uploads إذا لم يكن موجوداً
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== الصفحة الرئيسية ====================
@app.route('/')
def index():
    """الصفحة الرئيسية - لوحة التحكم"""
    try:
        # جلب سعر الذهب الفوري
        gold_data = get_gold_price()
        current_price = gold_data.get('price', 'N/A')
        price_change = gold_data.get('change', 'N/A')
        
        # جلب الأخبار الاقتصادية
        news_data = get_news()
        
        return render_template('index.html',
            current_price=current_price,
            price_change=price_change,
            news_data=news_data,
            now=datetime.now()
        )
    except Exception as e:
        return render_template('index.html',
            current_price='Error',
            price_change='Error',
            news_data=[],
            now=datetime.now(),
            error=str(e)
        )

# ==================== صفحة AI Analyzer ====================
@app.route('/ai-analyze')
def ai_analyze_page():
    """صفحة تحليل الشارت بالذكاء الاصطناعي"""
    return render_template('ai_analyse.html')

# ==================== تحليل الصورة ====================
@app.route('/ai-analyze', methods=['POST'])
def ai_analyze():
    """استقبال الصورة وتحليلها بـ Gemini"""
    # التحقق من وجود صورة
    if 'chart_image' not in request.files:
        return jsonify({'error': 'الرجاء رفع صورة الشارت'}), 400
    
    file = request.files['chart_image']
    
    if file.filename == '':
        return jsonify({'error': 'الرجاء اختيار صورة'}), 400
    
    if file and allowed_file(file.filename):
        # حفظ الصورة مؤقتاً
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # تحليل الصورة باستخدام Gemini
            analysis_result = analyze_chart_with_gemini(filepath)
            
            # حذف الصورة بعد التحليل
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify({
                'success': True,
                'analysis': analysis_result
            })
            
        except Exception as e:
            # حذف الصورة في حالة الخطأ
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'خطأ في التحليل: {str(e)}'}), 500
    
    return jsonify({'error': 'نوع الملف غير مدعوم. استخدم PNG, JPG, JPEG, WEBP, أو GIF'}), 400

# ==================== API جلب سعر الذهب ====================
@app.route('/api/gold-price')
def api_gold_price():
    """API لجلب سعر الذهب الفوري"""
    try:
        gold_data = get_gold_price()
        return jsonify(gold_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== API جلب الأخبار ====================
@app.route('/api/news')
def api_news():
    """API لجلب الأخبار الاقتصادية"""
    try:
        news_data = get_news()
        return jsonify(news_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== تشغيل السيرفر ====================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)