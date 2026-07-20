"""
جلب سعر الذهب الفوري من API
"""

import requests
import json
import logging

logger = logging.getLogger(__name__)

def get_gold_price():
    """
    جلب سعر الذهب الفوري (XAUUSD)
    
    Returns:
        dict: {'price': float, 'change': float}
    """
    try:
        # استخدام API مجاني (مثال: GoldAPI أو أي مصدر آخر)
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            price = data.get('price', 0)
            change = data.get('change', 0)
            
            return {
                'price': round(price, 2),
                'change': round(change, 2)
            }
        else:
            logger.error(f"Error fetching gold price: {response.status_code}")
            return {'price': 'N/A', 'change': 'N/A'}
            
    except Exception as e:
        logger.error(f"Error fetching gold price: {str(e)}")
        return {'price': 'N/A', 'change': 'N/A'}