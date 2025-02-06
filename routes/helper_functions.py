from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages

def article_template(function, key_name):
    
    try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key(key_name, language, today)


            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = function(True, language)

            if result and is_valid_article_data(result):

                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")

                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def multi_article_template(function, key_name):
    
    try:
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key(key_name, language, today)
        
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Creation of new event loop: manager handles and coordinates mult tasks
            loop = asyncio.new_event_loop()
        # Tells python to use this loop as the current event loop for the thread
            asyncio.set_event_loop(loop)
        # Run the event loop until it reaches completion in this case fetch_world_news
            results = loop.run_until_complete(function(language))
        # then we clean up the loop
            loop.close()

            if results and is_valid_article_data(results):
                with cache_lock:
                    cache[cache_key] = results
                    print(f"Cached result for {cache_key}")
                return jsonify(results)
            else:
                return jsonify({"error": "No result found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    