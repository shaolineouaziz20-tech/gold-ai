"""
جلب الأخبار الاقتصادية من Forex Factory
"""

import requests
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_news():
    """
    جلب الأخبار الاقتصادية عالية التأثير
    
    Returns:
        list: قائمة بالأخبار
    """
    try:
        # استخدام API مجاني للأخبار الاقتصادية
        # هذا مثال باستخدام API وهمي، استبدله بمصدر حقيقي
        url = "https://api.example.com/forex-news"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('news', [])
        else:
            logger.error(f"Error fetching news: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return []