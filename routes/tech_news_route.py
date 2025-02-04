from methods.tech_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages

async def fetch_tech_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(techcrunch_pick_of_day, True, language),
        fetch_article(zdnet_pick_of_day, True, language),
        fetch_article(wired_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

def tech_news_register_routes(app):
    @app.route('/wired-pick-of-day', methods=['GET'])
    def scrape_article():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            # Daily Inital Cache
            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('wired', language, today)

            # Check cache first
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # If not in cache, fetch new data
            result = wired_pick_of_day(True, language)
            
            if result and is_valid_article_data(result):
                # Store in cache
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/wired-pick-of-day-text', methods=['GET'])
    def scrape_article_text():
        result = wired_pick_of_day(False)
        return jsonify(result)

    @app.route('/techcrunch-pick-of-day', methods=['GET'])
    def scape_article15():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('techcrunch', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = techcrunch_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/techcrunch-pick-of-day-text', methods=['GET'])
    def scape_article15_text():
        result = techcrunch_pick_of_day(False)
        return jsonify(result)

    @app.route('/zdnet-pick-of-day', methods=['GET'])
    def scape_article16():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('zdnet', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = zdnet_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/tech-news', methods=['GET'])
    def scape_article17():
        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('tech-news', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_tech_news(language))
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

    @app.route('/tech-news-text', methods=['GET'])
    def scape_article17_text():
        return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False)])
