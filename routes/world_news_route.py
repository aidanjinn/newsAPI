from methods.world_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages

'''
    Async function for fetching news articles in the world news category
        This pattern allows for all news sources to be fetched and run
        simultaneously rather than one after another, reducing the total
        response time: This was done in order to cut down on awaiting
        LLM response from prompt request.
'''
   
async def fetch_world_news(language):
  
    async def fetch_article(func, *args):
    
        return await asyncio.to_thread(func, *args)
        
     # these are the list of tasks to run concurrently
    tasks = [
        fetch_article(AP_pick_of_day, True, language),
        fetch_article(democracy_now_pick_of_day, True, language),
        fetch_article(SCMP_pick_of_day, True, language),
        fetch_article(SCMP_china, True, language)
    ]

    return await asyncio.gather(*tasks)

def world_news_register_routes(app):

    @app.route('/AP-pick-of-day', methods=['GET'])
    def scape_article2():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('ap', language, today)


            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = AP_pick_of_day(True, language)

            if result and is_valid_article_data(result):

                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")

                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/AP-pick-of-day-text', methods=['GET'])
    def scrape_article2_text():

        result = AP_pick_of_day(False)

        return jsonify(result)

    
    @app.route('/democracy-now-pick-of-day', methods=['GET'])
    def scape_article9():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('democracy-now', language, today)
        
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = democracy_now_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/democracy-now-pick-of-day-text', methods=['GET'])
    def scape_article9_text():

        result = democracy_now_pick_of_day(False)

        return jsonify(result)

    @app.route('/world-news', methods=['GET'])
    def scape_article10():
        try:
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('world-news', language, today)
        
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
            results = loop.run_until_complete(fetch_world_news(language))
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


    @app.route('/world-news-text', methods=['GET'])
    def scape_article10_text():

        return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False), SCMP_china(False)])

    @app.route('/SCMP-pick-of-day', methods=['GET'])
    def scape_article11():

        try:
            # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('SCMP-pick', language, today)
            
            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = SCMP_pick_of_day(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/SCMP-pick-of-day-text', methods=['GET'])
    def scape_article11_text():

        result = SCMP_pick_of_day(False)

        return jsonify(result)  

    @app.route('/SCMP-china-top-story', methods=['GET'])
    def scape_article12():

        try:
        # Get the language query parameter, default to 'english'
            language = request.args.get('language', default='english').lower()

            default=('english').lower()
            today = datetime.now().strftime("%Y%m%d")
            cache_key = get_cache_key('SCMP-china', language, today)

            with cache_lock:
                if cache_key in cache:
                    print(f"Cache hit for {cache_key}")
                    enforce_cache_limit()
                    return jsonify(cache[cache_key])

            if language not in supported_languages:
                return jsonify({"error": f"Language '{language}' is not supported."}), 400

            # Default Behavior is AI-SUM ON; ENGLISH
            result = SCMP_china(True, language)

            if result and is_valid_article_data(result):
                with cache_lock:
                    cache[cache_key] = result
                    print(f"Cached result for {cache_key}")
                return jsonify(result)
            else:
                return jsonify({"error": "No result found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/SCMP-china-top-story-text', methods=['GET'])
    def scape_article12_text():

        result = SCMP_china(False)

        return jsonify(result)