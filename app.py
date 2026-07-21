from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from services.gold_price import get_gold_price
from services.forex_factory import get_news

app = Flask(__name__)

# ====== UPLOAD SETTINGS ======
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ====== HOME PAGE ======
@app.route('/')
def index():
    gold_data = get_gold_price()
    current_price = gold_data.get('price', 'N/A')
    price_change = gold_data.get('change', 'N/A')
    news_data = get_news()
    
    return render_template('index.html',
        current_price=current_price,
        price_change=price_change,
        news_data=news_data,
        now=datetime.now()
    )

# ====== NEWS PAGE ======
@app.route('/news')
def news_page():
    gold_data = get_gold_price()
    current_price = gold_data.get('price', 'N/A')
    price_change = gold_data.get('change', 'N/A')
    news_data = get_news()
    
    session_bias = "NEUTRAL"
    confidence = 0
    bias_reason = "في انتظار تحليل البيانات..."
    dol_target = "في انتظار التحليل..."
    dol_reason = "سيتم تحديده بناء على الأخبار"
    
    return render_template('news.html',
        current_price=current_price,
        price_change=price_change,
        news_data=news_data,
        session_bias=session_bias,
        confidence=confidence,
        bias_reason=bias_reason,
        dol_target=dol_target,
        dol_reason=dol_reason,
        now=datetime.now()
    )

# ====== AI ANALYZE PAGE ======
@app.route('/ai-analyze')
def ai_analyze_page():
    return render_template('ai_analyse.html')

# ====== AI ANALYZE (POST) ======
@app.route('/ai-analyze', methods=['POST'])
def ai_analyze():
    try:
        if 'chart_image' not in request.files:
            return jsonify({'error': 'الرجاء رفع صورة'}), 400
        
        file = request.files['chart_image']
        if file.filename == '':
            return jsonify({'error': 'الرجاء اختيار صورة'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'نوع الملف غير مدعوم'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            from services.ai_engine import analyze_chart_with_gemini
            result = analyze_chart_with_gemini(filepath)
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'success': True,
                'analysis': result.encode('utf-8', 'ignore').decode('utf-8')
            })
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'خطأ في التحليل: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'خطأ عام: {str(e)}'}), 500

# ====== API GET GOLD PRICE ======
@app.route('/api/gold-price')
def api_gold_price():
    try:
        data = get_gold_price()
        return jsonify({
            'price': data.get('price', 'N/A'),
            'change': data.get('change', 'N/A')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ====== RUN ======
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)