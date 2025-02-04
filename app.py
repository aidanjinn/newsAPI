from flask import Flask, jsonify, request, render_template
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

from methods.entertainment_news import *
from methods.fashion_news import *
from methods.finance_news import *
from methods.sports_news import *
from methods.tech_news import *
from methods.weather_news import *
from methods.world_news import *

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

supported_languages = [
    'english', 'spanish', 'french', 'chinese', 'japanese', 'hindi', 'arabic', 'portuguese',
    'russian', 'german', 'italian', 'korean', 'bulgarian', 'croatian', 'czech', 'danish',
    'dutch', 'swedish', 'norwegian', 'finnish', 'polish', 'bengali', 'greek', 'thai',
    'vietnamese', 'indonesian', 'hebrew', 'turkish', 'ukrainian', 'romanian', 'slovak',
    'slovenian', 'serbian', 'bosnian', 'hungarian', 'tagalog', 'urdu', 'swahili', 'amharic',
    'somali', 'haitian creole', 'lao', 'khmer', 'burmese', 'sinhalese', 'malay',
    'macedonian', 'pidgin', 'catalon', 'flemish', 'dutch', 'afrikaans'
]

cache_thread = threading.Thread(target=clear_old_cache, daemon=True)
cache_thread.start()

# new main page route for easier testing
@app.route('/', methods=['GET'])
def index():
    # List of supported routes (you can dynamically generate this if needed)
    supported_routes = [
        '/wired-pick-of-day',
      
        '/AP-pick-of-day',
       
        '/vogue-pick-of-day',
       
        '/rolling-stone-movies-tv-pick-of-day',
     
        '/yahoo-sports-pick-of-day',
       
        '/yahoo-sports-breaking-news',
       
        '/yahoo-sports',
      
        '/yahoo-sports-recap',
     
        '/democracy-now-pick-of-day',
       
        '/world-news',
  
        '/SCMP-pick-of-day',
      
        '/SCMP-china-top-story',
  
        '/cosmo-style-pick-of-day',
      
        '/fashion-news',
     
        '/techcrunch-pick-of-day',
     
        '/zdnet-pick-of-day',

        '/tech-news',
      
        '/weather-channel-pick-of-day',
     
        '/weather-gov-pick-of-day',

        '/weather-news',
    
        '/yahoo-finance-pick-of-day',
      
        '/economist-pick-of-day',
       
        '/forbes-pick-of-day',
  
        '/finance-news',
   
        '/people-pick-of-day',
    
        '/entertainment-news'
    ] 
    return render_template('index.html', supported_routes=supported_routes, supported_languages=supported_languages)


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

@app.route('/vogue-pick-of-day', methods=['GET'])
def scape_article3():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('vogue', language, today)


        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = vogue_pick_of_day(True, language)

        if result and is_valid_article_data(result):

            with cache_lock:
                cache[cache_key] = result
                print(f"Cached result for {cache_key}")

            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vogue-pick-of-day-text', methods=['GET'])
def scape_article3_text():

    result = vogue_pick_of_day(False)

    return jsonify(result)

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

@app.route('/yahoo-sports-pick-of-day', methods=['GET'])
def scape_article5():

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
def scape_article5_text():

    result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", False)

    return jsonify(result)

@app.route('/yahoo-sports-breaking-news', methods=['GET'])
def scape_article6():

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
def scape_article6_text():

    result = yahoo_sports_breaking_news(False)

    return jsonify(result)

@app.route('/yahoo-sports', methods=['GET'])
def scape_article7():

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
def scape_article7_text():

    breaking_news = yahoo_sports_breaking_news(False)
    pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/",False)

    if breaking_news:
        result = [breaking_news, pick_of_day]
    else:
        result = [pick_of_day]

    return jsonify(result)


@app.route('/yahoo-sports-recap', methods = ['GET'])
def scrape_article8():
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

async def fetch_yahoo_sports_recap(urls, language):
    async def fetch_article(url):
        return await asyncio.to_thread(yahoo_sports_pick_of_day, url, True, language)
    
    tasks = [fetch_article(url) for url in urls]
    return await asyncio.gather(*tasks)

@app.route('/yahoo-sports-recap-text', methods = ['GET'])
def scrape_article8_text():

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

'''
    Async function for fetching news articles in the world news category
        This pattern allows for all news sources to be fetched and run
        simultaneously rather than one after another, reducing the total
        response time: This was done in order to cut down on awaiting
        LLM response from prompt request.
'''
async def fetch_world_news(language):
    
    # helper function that takes any sync function and it arguments
    async def fetch_article(func, *args):
        # runs the sync function in a thread and returns its result
        return await asyncio.to_thread(func, *args)
    
    # these are the list of tasks to run concurrently
    tasks = [
        fetch_article(AP_pick_of_day, True, language),
        fetch_article(democracy_now_pick_of_day, True, language),
        fetch_article(SCMP_pick_of_day, True, language)
    ]
    # gather here runs all the tasks concurrently and then waits for their completion
    return await asyncio.gather(*tasks)

@app.route('/world-news-text', methods=['GET'])
def scape_article10_text():

    return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False)])

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


@app.route('/cosmo-style-pick-of-day', methods=['GET'])
def scape_article13():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('cosmo', language, today)
        
        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = cosmo_style(True, language)

        if result and is_valid_article_data(result): 
            with cache_lock:
                cache[cache_key] = result
                print(f"Cached result for {cache_key}")
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cosmo-style-pick-of-day-text', methods=['GET'])
def scape_article13_text():

    result = cosmo_style(False)

    return jsonify(result)

@app.route('/fashion-news', methods=['GET'])
def scape_article14():
    try:
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('fashion', language, today)

        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(fetch_fashion_news(language))
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

async def fetch_fashion_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(vogue_pick_of_day, True, language),
        fetch_article(cosmo_style, True, language)
    ]
    return await asyncio.gather(*tasks)

@app.route('/fashion-news-text', methods=['GET'])
def scape_article14_text():

    return jsonify([vogue_pick_of_day(False), cosmo_style(False)])

@app.route('/techcrunch-pick-of-day', methods=['GET'])
def scape_article15():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('techcrunch', language, today)

        with cache_lock and is_valid_article_data(result):
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = techcrunch_pick_of_day(True, language)

        if result:
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

async def fetch_tech_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(techcrunch_pick_of_day, True, language),
        fetch_article(zdnet_pick_of_day, True, language),
        fetch_article(wired_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

@app.route('/tech-news-text', methods=['GET'])
def scape_article17_text():

    return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False)])

@app.route('/weather-channel-pick-of-day', methods=['GET'])
def scape_article18():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('weather-channel', language, today)

        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = weather_channel_pick_of_day(True, language)

        if result and is_valid_article_data(result):
            with cache_lock:
                cache[cache_key] = result
                print(f"Cached result for {cache_key}")
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather-channel-pick-of-day-text', methods=['GET'])
def scape_article18_text():

    result = weather_channel_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-gov-pick-of-day', methods=['GET'])
def scape_article19():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('weather-gov', language, today)

        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = weather_gov_pick_of_day(True, language)

        if result and is_valid_article_data(result):
            with cache_lock:
                cache[cache_key] = result
                print(f"Cached result for {cache_key}")
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather-gov-pick-of-day-text', methods=['GET'])
def scape_article19_text():

    result = weather_gov_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-news', methods=['GET'])
def scape_article20():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        default=('english').lower()
        today = datetime.now().strftime("%Y%m%d")
        cache_key = get_cache_key('weather-news', language, today)

        with cache_lock:
            if cache_key in cache:
                print(f"Cache hit for {cache_key}")
                enforce_cache_limit()
                return jsonify(cache[cache_key])

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(fetch_weather_news(language))
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

async def fetch_weather_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(weather_channel_pick_of_day, True, language),
        fetch_article(weather_gov_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

@app.route('/weather-news-text', methods=['GET'])
def scape_article20_text():

    return jsonify([weather_channel_pick_of_day(False),weather_gov_pick_of_day(False)])

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

async def fetch_finance_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(yahoo_finance_pick_of_day, True, language),
        fetch_article(economist_pick_of_day, True, language),
        fetch_article(forbes_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

@app.route('/finance-news-text', methods=['GET'])
def scape_article24_text():

    return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False)])

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

async def fetch_entertainment_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(rolling_stone_pick_of_day, True, language),
        fetch_article(people_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

@app.route('/entertainment-news-text', methods=['GET'])
def scape_article26_text():

    return jsonify([rolling_stone_pick_of_day(False), people_pick_of_day(False)])

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
    next_clear = get_next_cache_clear_time(now)
    
    time_remaining = (next_clear - now).total_seconds()
    hours, remainder = divmod(int(time_remaining), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    stats = {
        'memory_usage_mb': process.memory_info().rss / 1024 / 1024,
        'memory_percent': process.memory_percent(),
        'cache_entries': len(cache),
        'cache_keys': list(cache.keys()),
        'cache_size_mb': get_cache_size() / 1024 / 1024,
        'cpu_percent': process.cpu_percent(),
        'next_cache_clear': next_clear.strftime("%Y-%m-%d %H:%M:%S"),
        'time_until_clear': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
