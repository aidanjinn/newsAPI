from methods.finance_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages

async def fetch_finance_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(yahoo_finance_pick_of_day, True, language),
        fetch_article(economist_pick_of_day, True, language),
        fetch_article(forbes_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

def finance_news_register_routes(app):
    
    @app.route('/yahoo-finance-pick-of-day', methods=['GET'])
    def scape_article21():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('yahoo-finance', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = yahoo_finance_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/yahoo-finance-pick-of-day-text', methods=['GET'])
    def scape_article21_text():

        result = yahoo_finance_pick_of_day(False)

        return jsonify(result)

    @app.route('/economist-pick-of-day', methods=['GET'])
    def scape_article22():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('economist-pick', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = economist_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/economist-pick-of-day-text', methods=['GET'])
    def scape_article22_text():

        result = economist_pick_of_day(False)

        return jsonify(result)

    @app.route('/forbes-pick-of-day', methods=['GET'])
    def scape_article23():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('forbes-pick', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = forbes_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/forbes-pick-of-day-text', methods=['GET'])
    def scape_article23_text():

        result = forbes_pick_of_day(False)

        return jsonify(result)

    @app.route('/finance-news', methods=['GET'])
    def scape_article24():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('finance-news', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_finance_news(language))
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

    @app.route('/finance-news-text', methods=['GET'])
    def scape_article24_text():

        return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False)])
