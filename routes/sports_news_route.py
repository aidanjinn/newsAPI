from methods.sports_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

async def fetch_yahoo_sports_recap(urls, language):
    async def fetch_article(url):
        return await asyncio.to_thread(yahoo_sports_pick_of_day, url, True, language)
    
    tasks = [fetch_article(url) for url in urls]
    return await asyncio.gather(*tasks)

def sports_news_register_routes(app):
    
    @app.route('/yahoo-sports-pick-of-day', methods=['GET'])
    def scrape_article_yahoo_sports_pick():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('yahoo-sports-pick', language, today)
        
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = yahoo_sports_pick_of_day("https://sports.yahoo.com", True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/yahoo-sports-pick-of-day-text', methods=['GET'])
    def scrape_article_yahoo_sports_pick_text():

        result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", False)

        return jsonify(result)

    @app.route('/yahoo-sports-breaking-news', methods=['GET'])
    def scrape_article_yahoo_sport_breaking_news():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = yahoo_sports_breaking_news(True, language)

            if result:
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/yahoo-sports-breaking-news-text', methods=['GET'])
    def scrape_article_yahoo_sports_breaking_news_text():

        result = yahoo_sports_breaking_news(False)

        return jsonify(result)

    @app.route('/yahoo-sports', methods=['GET'])
    def scrape_article_yahoo_sports():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('yahoo-sports', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Fetch breaking news and pick of the day in the specified language
            breaking_news = yahoo_sports_breaking_news(True, language)
            pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/", True, language)

            # Combine results, include breaking news only if it's available
            result = [breaking_news, pick_of_day] if breaking_news else [pick_of_day]
            if result and is_valid_article_data(result):
                with cache_lock:
                        cache[cache_key] = result
                        print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/yahoo-sports-text', methods=['GET'])
    def scrape_article_yahoo_sports_text():

        breaking_news = yahoo_sports_breaking_news(False)
        pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/",False)

        if breaking_news:
            result = [breaking_news, pick_of_day]
        else:
            result = [pick_of_day]

        return jsonify(result)


    @app.route('/yahoo-sports-recap', methods = ['GET'])
    def scrape_article_yahoo_sport_recap():
        urls = [
            "https://sports.yahoo.com/nfl/",
            "https://sports.yahoo.com/college-football/",
            "https://sports.yahoo.com/nba/",
            "https://sports.yahoo.com/nhl/",
            "https://sports.yahoo.com/college-basketball/",
            "https://sports.yahoo.com/college-womens-basketball/",
            "https://sports.yahoo.com/mlb/"
        ]

        try:
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('yahoo-sports-recap', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_yahoo_sports_recap(urls, language))
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

    @app.route('/yahoo-sports-recap-text', methods = ['GET'])
    def scrape_article_yahoo_sports_recap_text():

        urls = [
            "https://sports.yahoo.com/nfl/",
            "https://sports.yahoo.com/college-football/",
            "https://sports.yahoo.com/nba/",
            "https://sports.yahoo.com/nhl/",
            "https://sports.yahoo.com/college-basketball/",
            "https://sports.yahoo.com/college-womens-basketball/",
            "https://sports.yahoo.com/mlb/"
        ]

        result = []
        for url in urls:
            result.append(yahoo_sports_pick_of_day(url,False))

        return jsonify(result)