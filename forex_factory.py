import requests
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_news():
    """
    جلب الأخبار الاقتصادية الحقيقية المؤثرة على XAUUSD
    """
    try:
        # ====== استخدم API حقيقي ======
        # 1. ForexFactory API (مجاني)
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # فلترة الأخبار لي عندها علاقة بالذهب
            gold_related = []
            keywords = ['gold', 'xau', 'inflation', 'fed', 'interest rate', 'dollar', 'usd', 'cpi', 'ppi', 'unemployment']
            
            for item in data:
                title = item.get('title', '').lower()
                country = item.get('country', '').upper()
                
                # الأخبار الأمريكية فقط (تأثير كبير على الذهب)
                if country == 'US':
                    for keyword in keywords:
                        if keyword in title:
                            # تحليل تأثير الخبر
                            impact = item.get('impact', 'low').lower()
                            forecast = item.get('forecast', 'N/A')
                            previous = item.get('previous', 'N/A')
                            
                            # تحديد التأثير على الذهب
                            gold_impact, direction = analyze_news_impact(title, impact, forecast, previous)
                            
                            gold_related.append({
                                'title': item.get('title', 'Unknown'),
                                'impact': impact,
                                'time': item.get('time', 'N/A'),
                                'gold_impact': gold_impact,
                                'direction': direction,
                                'forecast': forecast,
                                'previous': previous,
                                'analysis': generate_analysis(title, impact, direction, gold_impact)
                            })
                            break
            
            # ترتيب حسب التأثير (الأعلى أولاً)
            gold_related.sort(key=lambda x: x['gold_impact'], reverse=True)
            
            return gold_related[:10]  # أهم 10 أخبار
            
        else:
            logger.warning("API failed, using fallback data")
            return get_fallback_news()
            
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return get_fallback_news()


def analyze_news_impact(title, impact, forecast, previous):
    """
    تحليل تأثير الخبر على الذهب
    """
    title_lower = title.lower()
    gold_impact = 0
    direction = 'neutral'
    
    # ====== تحديد قوة التأثير ======
    if impact == 'high':
        gold_impact = 7.0 + (float(forecast) if forecast != 'N/A' else 0) / 10
    elif impact == 'medium':
        gold_impact = 4.0 + (float(forecast) if forecast != 'N/A' else 0) / 20
    else:
        gold_impact = 1.5
    
    # ====== تحديد الاتجاه ======
    bullish_keywords = ['positive', 'increase', 'rise', 'high', 'better', 'above', 'growth']
    bearish_keywords = ['negative', 'decrease', 'fall', 'low', 'worse', 'below', 'decline']
    
    # تحليل الكلمات المفتاحية
    for word in bullish_keywords:
        if word in title_lower:
            direction = 'bullish'
            gold_impact += 1.5
            break
    
    for word in bearish_keywords:
        if word in title_lower:
            direction = 'bearish'
            gold_impact -= 1.5
            break
    
    # ====== تحليل المؤشرات الاقتصادية ======
    if 'inflation' in title_lower or 'cpi' in title_lower:
        direction = 'bullish' if 'high' in title_lower else 'bearish'
        gold_impact += 3.0
    
    if 'fed' in title_lower or 'interest rate' in title_lower:
        if 'hike' in title_lower or 'increase' in title_lower:
            direction = 'bearish'
            gold_impact += 4.0
        else:
            direction = 'bullish'
            gold_impact += 3.0
    
    if 'unemployment' in title_lower or 'jobless' in title_lower:
        if 'better' in title_lower or 'low' in title_lower:
            direction = 'bearish'
            gold_impact += 2.0
        else:
            direction = 'bullish'
            gold_impact += 2.0
    
    # تحديد الحد الأقصى
    gold_impact = min(max(gold_impact, 0.5), 15.0)
    
    return round(gold_impact, 1), direction


def generate_analysis(title, impact, direction, gold_impact):
    """
    توليد تحليل للخبر
    """
    if direction == 'bullish':
        direction_text = "🟢 صاعد (Bullish)"
    elif direction == 'bearish':
        direction_text = "🔴 هابط (Bearish)"
    else:
        direction_text = "🟡 محايد (Neutral)"
    
    return f"""
    📊 الخبر: {title}
    📈 التأثير: {direction_text}
    💰 نسبة التأثير على الذهب: {gold_impact}%
    """


def get_fallback_news():
    """
    بيانات احتياطية في حالة فشل API
    """
    return [
        {
            'title': 'US Federal Reserve Interest Rate Decision',
            'impact': 'high',
            'time': datetime.now().strftime('%H:%M'),
            'gold_impact': 8.5,
            'direction': 'bearish',
            'analysis': '📊 زيادة سعر الفائدة = 💰 انخفاض الذهب (Bearish)'
        },
        {
            'title': 'US CPI Inflation Data Release',
            'impact': 'high',
            'time': datetime.now().strftime('%H:%M'),
            'gold_impact': 7.2,
            'direction': 'bullish',
            'analysis': '📊 ارتفاع التضخم = 💰 زيادة الطلب على الذهب (Bullish)'
        },
        {
            'title': 'US Jobless Claims - Better than expected',
            'impact': 'medium',
            'time': datetime.now().strftime('%H:%M'),
            'gold_impact': 4.5,
            'direction': 'bearish',
            'analysis': '📊 تحسن سوق العمل = 💰 ضعف الذهب (Bearish)'
        }
    ]