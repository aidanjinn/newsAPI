from flask import Flask, jsonify, request, render_template
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

from routes.world_news_route import world_news_register_routes
from routes.weather_news_route import weather_news_register_routes
from routes.tech_news_route import tech_news_register_routes
from routes.sports_news_route import sports_news_register_routes
from routes.finance_news_route import finance_news_register_routes
from routes.fashion_news_route import fashion_news_register_routes
from routes.entertainment_news_route import entertainment_news_register_routes

from config import supported_languages
from config import supported_routes

from datetime import datetime, timedelta
import threading
import time
from methods.cache import *
import psutil
import os

from flask_cors import CORS

'''
[JSON Object Fields]
@ Website Link:
@ Summary:
'''

app = Flask(__name__)

CORS(app)

world_news_register_routes(app)
weather_news_register_routes(app)
tech_news_register_routes(app)
sports_news_register_routes(app)
finance_news_register_routes(app)
fashion_news_register_routes(app)
entertainment_news_register_routes(app)


cache_thread = threading.Thread(target=clear_old_cache, daemon=True)
cache_thread.start()

'''
    Main Page Route: Sets up drop downs to ping supported routes
'''
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html', supported_routes=supported_routes, supported_languages=supported_languages)


@app.route('/clear-cache', methods=['POST'])
def clear_specific_cache():
    try:
        data = request.get_json()
        route = data.get('route')
        language = data.get('language', 'english').lower()
        
        if not route:
            return jsonify({"error": "Route parameter is required"}), 400
            
        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported"}), 400
            
        success = clear_cache_key(route, language)
        if success:
            return jsonify({"message": f"Cache cleared for {route} in {language}"})
        else:
            return jsonify({"message": f"No cache entry found for {route} in {language}"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/memory-stats', methods=['GET'])
def memory_stats():
    process = psutil.Process(os.getpid())
    now = datetime.now()
    
    current_clear_time = None
    with next_cache_clear_lock:
        current_clear_time = next_cache_clear or get_next_cache_clear_time()
    
    time_remaining = max(0, (current_clear_time - now).total_seconds())
    hours, remainder = divmod(int(time_remaining), 3600)
    minutes, seconds = divmod(remainder, 60)

    stats = {
        'memory_usage_mb': round(process.memory_info().rss / 1024 / 1024, 2),
        'memory_percent': round(process.memory_percent(), 2),
        'cache_entries': len(cache),
        'cache_keys': list(cache.keys()),
        'cache_size_mb': round(get_cache_size() / 1024 / 1024, 2),
        'cpu_percent': round(process.cpu_percent(), 2),
        'next_cache_clear': current_clear_time.strftime("%Y-%m-%d %H:%M:%S"),
        'time_until_clear': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
        'current_time': now.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)
