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

# Add this at the top with other globals
next_cache_clear = None
def get_next_cache_clear_time(current_time=None):
    """Calculate the next cache clear time based on current time."""
    now = current_time or datetime.now()
    
    # Cache set to clear every 4 hours
    next_clear = (now + timedelta(hours=4)).replace(second=0, microsecond=0)
    
    return next_clear

# Modify clear_old_cache to use the new function
def clear_old_cache():
    """Clear cache every 4 hours"""
    global next_cache_clear
    while True:
        now = datetime.now()
        with cache_lock:
            cache.clear()
            print(f"Cache cleared at {now}")
        
        next_clear = get_next_cache_clear_time(now)
        next_cache_clear = next_clear
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