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

def multi_template(function, key_name):
    language = request.args.get('language', default='english').lower()

    if language not in supported_languages:
        return jsonify({"error": f"Language '{language}' is not supported."}), 400

    today = datetime.now().strftime("%Y%m%d")
    cache_key = get_cache_key(key_name, language, today)

    with cache_lock:
        if cache_key in cache:
            print(f"Cache hit for {cache_key}")
            enforce_cache_limit()
            return jsonify(cache[cache_key])

    results = asyncio.run(function(language))

    json = []
    for response in results:
        json.append(response.get_json())

    if is_valid_article_data(json):
        with cache_lock:
            cache[cache_key] = json
            enforce_cache_limit()

    return jsonify(json)
    
    