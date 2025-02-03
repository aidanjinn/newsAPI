from datetime import datetime, timedelta
import threading
import time

cache = {}
CACHE_LIMIT = 100 * 1024 * 1024  # 100MB
cache_lock = threading.Lock()

def get_cache_key(route, language, date):
    return f"{route}_{language}_{date}"

def clear_old_cache():
    """Clear cache four times a day: 6 AM, 12 PM, 8 PM, and midnight."""
    while True:
        now = datetime.now()
        with cache_lock:
            cache.clear()
            print(f"Cache cleared at {now}")
        
        # Calculate next clearing time
        if now.hour < 6:
            next_clear = now.replace(hour=6, minute=0, second=0, microsecond=0)
        elif now.hour < 12:
            next_clear = now.replace(hour=12, minute=0, second=0, microsecond=0)
        elif now.hour < 20:
            next_clear = now.replace(hour=20, minute=0, second=0, microsecond=0)
        else:
            next_clear = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        sleep_seconds = (next_clear - now).total_seconds()
        time.sleep(sleep_seconds)

def clear_cache_key(route, language):
    """Clear a specific cache entry."""
    today = datetime.now().strftime("%Y%m%d")
    cache_key = get_cache_key(route, language, today)
    with cache_lock:
        if cache_key in cache:
            del cache[cache_key]
            return True
        return False


def is_valid_article_data(data):
    """Validate article data before caching."""
    if not isinstance(data, dict) and not isinstance(data, list):
        return False
        
    def check_article(article):
        return (isinstance(article, dict) 
                and article.get('article_link') 
                and article.get('article_title') 
                and article.get('article_text')
                and all(isinstance(v, str) for v in [
                    article['article_link'], 
                    article['article_title'], 
                    article['article_text']
                ]))
    
    if isinstance(data, list):
        return all(check_article(article) for article in data)
    return check_article(data)