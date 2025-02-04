from datetime import datetime, timedelta
import threading
import time

cache = {}
CACHE_LIMIT = 150 * 1024 * 1024  
cache_lock = threading.Lock()

def get_cache_size():
    """Calculate current cache size in bytes"""
    import sys
    size = 0
    for key, value in cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size

def enforce_cache_limit():
    """Remove oldest entries if cache exceeds size limit"""
    while get_cache_size() > CACHE_LIMIT and cache:
        # Remove oldest entry (first item in cache)
        oldest_key = next(iter(cache))
        del cache[oldest_key]
        print(f"Removed {oldest_key} from cache due to size limit")

def get_cache_key(route, language, date):
    return f"{route}_{language}_{date}"


next_cache_clear = None
next_cache_clear_lock = threading.Lock()

def get_next_cache_clear_time(current_time=None):
    """Calculate the next cache clear time based on current time."""
    now = current_time or datetime.now()
    hours = now.hour
    next_interval = ((hours // 4) + 1) * 4
    next_clear = now.replace(hour=next_interval % 24, minute=0, second=0, microsecond=0)
    
    if next_clear <= now:
        next_clear += timedelta(hours=4)
    
    return next_clear


def clear_old_cache():
    """Clear cache every 4 hours in a thread-safe manner."""
    global next_cache_clear
    
    with next_cache_clear_lock:
        next_cache_clear = get_next_cache_clear_time()
    
    while True:
        now = datetime.now()
        current_clear_time = None
        
        with next_cache_clear_lock:
            current_clear_time = next_cache_clear
            
            if now >= current_clear_time:
                with cache_lock:
                    cache.clear()
                    print(f"Cache cleared at {now}")
                next_cache_clear = get_next_cache_clear_time(now)
        
        # Sleep for a shorter interval to be more responsive
        time.sleep(10)

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