from methods.entertainment_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages

async def fetch_entertainment_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(rolling_stone_pick_of_day, True, language),
        fetch_article(people_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

def entertainment_news_register_routes(app):
    
    @app.route('/rolling-stone-movies-tv-pick-of-day', methods=['GET'])
    def scape_article4():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('rolling-stone', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = rolling_stone_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/rolling-stone-movies-tv-pick-of-day-text', methods=['GET'])
    def scape_article4_text():

        result = rolling_stone_pick_of_day(False)

        return jsonify(result)

    @app.route('/people-pick-of-day', methods=['GET'])
    def scape_article25():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('people-pick', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = people_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/people-pick-of-day-text', methods=['GET'])
    def scape_article25_text():

        result = people_pick_of_day(False)

        return jsonify(result)

    @app.route('/entertainment-news', methods=['GET'])
    def scape_article26():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('entertainment', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_entertainment_news(language))
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

    @app.route('/entertainment-news-text', methods=['GET'])
    def scape_article26_text():

        return jsonify([rolling_stone_pick_of_day(False), people_pick_of_day(False)])
