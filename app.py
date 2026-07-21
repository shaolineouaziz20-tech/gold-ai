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
    news_data = get_news()
    
    # تحديد Daily Bias بناء على الأخبار (مثال)
    daily_bias = "Bullish"
    bias_reason = "Positive economic data supporting gold prices"
    
    # تحليل تأثير كل خبر على الذهب
    for news in news_data:
        if news.get('impact', '').lower() == 'high':
            news['analysis'] = "High impact - Expect significant volatility in gold prices"
        elif news.get('impact', '').lower() == 'medium':
            news['analysis'] = "Medium impact - Possible short-term price movement"
        else:
            news['analysis'] = "Low impact - Minimal effect on gold prices"
    
    return render_template('news.html',
        news_data=news_data,
        daily_bias=daily_bias,
        bias_reason=bias_reason,
        now=datetime.now()
    )

# ====== AI ANALYZE PAGE ======
@app.route('/ai-analyze')
def ai_analyze_page():
    return render_template('ai_analyse.html')

# ====== AI ANALYZE (POST) ======
@app.route('/ai-analyze', methods=['POST'])
def ai_analyze():
    if 'chart_image' not in request.files:
        return jsonify({'error': 'الرجاء رفع صورة'}), 400
    
    file = request.files['chart_image']
    if file.filename == '':
        return jsonify({'error': 'الرجاء اختيار صورة'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            from services.ai_engine import analyze_chart_with_gemini
            result = analyze_chart_with_gemini(filepath)
            os.remove(filepath)
            return jsonify({'success': True, 'analysis': result})
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'خطأ: {str(e)}'}), 500
    
    return jsonify({'error': 'نوع الملف غير مدعوم'}), 400

# ====== API GET GOLD PRICE ======
@app.route('/api/gold-price')
def api_gold_price():
    """جلب سعر الذهب فوري عبر API"""
    try:
        from services.gold_price import get_gold_price
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