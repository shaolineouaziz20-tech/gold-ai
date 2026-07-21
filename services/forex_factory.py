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
        # استخدم API مجاني للأخبار (مثال: ForexFactory أو AlphaVantage)
        # هادا مثال باستخدام بيانات وهمية محسنة
        news_list = [
            {
                'title': 'US Federal Reserve Interest Rate Decision',
                'impact': 'high',
                'time': (datetime.now() - timedelta(hours=2)).strftime('%H:%M'),
                'gold_impact': 8.5,
                'direction': 'bearish'
            },
            {
                'title': 'US CPI Inflation Data Release',
                'impact': 'high',
                'time': (datetime.now() - timedelta(hours=5)).strftime('%H:%M'),
                'gold_impact': 7.2,
                'direction': 'bullish'
            },
            {
                'title': 'US Jobless Claims - Better than expected',
                'impact': 'medium',
                'time': (datetime.now() - timedelta(hours=8)).strftime('%H:%M'),
                'gold_impact': 4.5,
                'direction': 'bearish'
            },
            {
                'title': 'Geopolitical Tensions - Middle East Update',
                'impact': 'medium',
                'time': (datetime.now() - timedelta(hours=10)).strftime('%H:%M'),
                'gold_impact': 6.8,
                'direction': 'bullish'
            },
            {
                'title': 'USD Index (DXY) Technical Analysis',
                'impact': 'low',
                'time': (datetime.now() - timedelta(hours=14)).strftime('%H:%M'),
                'gold_impact': 2.1,
                'direction': 'bearish'
            }
        ]
        
        return news_list
        
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return []