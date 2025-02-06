from methods.world_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

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
    tasks = [
        fetch_article(AP_pick_of_day, True, language),
        fetch_article(democracy_now_pick_of_day, True, language),
        fetch_article(SCMP_pick_of_day, True, language),
        fetch_article(SCMP_china, True, language),
        fetch_article(BBC_pick_of_day, True, language),
        fetch_article(NPR_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

def world_news_register_routes(app):

    @app.route('/AP-pick-of-day', methods=['GET'])
    def scrape_article_AP():
        return article_template(AP_pick_of_day, 'AP-pick')

    @app.route('/AP-pick-of-day-text', methods=['GET'])
    def scrape_article_AP_text():
        result = AP_pick_of_day(False)
        return jsonify(result)

    @app.route('/democracy-now-pick-of-day', methods=['GET'])
    def scrape_article_democracy():
        return article_template(democracy_now_pick_of_day, 'democracy-now-pick')

    @app.route('/democracy-now-pick-of-day-text', methods=['GET'])
    def scrape_article_democracy_text():
        result = democracy_now_pick_of_day(False)
        return jsonify(result)

    @app.route('/world-news', methods=['GET'])
    def scrape_article_world_news():
        return multi_article_template(fetch_world_news, 'world-news')

    @app.route('/world-news-text', methods=['GET'])
    def scrape_article_world_news_text():
        return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False), SCMP_china(False)])

    @app.route('/SCMP-pick-of-day', methods=['GET'])
    def scrape_article_SCMP():
        return  article_template(SCMP_pick_of_day, 'SCMP-pick')

    @app.route('/SCMP-pick-of-day-text', methods=['GET'])
    def scrape_article_SCMP_text():
        result = SCMP_pick_of_day(False)
        return jsonify(result)  

    @app.route('/SCMP-china-top-story', methods=['GET'])
    def scrape_article_SCMP_china():
        return  article_template(SCMP_china, 'SCMP-china')

    @app.route('/SCMP-china-top-story-text', methods=['GET'])
    def scrape_article_SCMP_china_text():
        result = SCMP_china(False)
        return jsonify(result)
    
    @app.route('/BBC-pick-of-day', methods=['GET'])
    def scrape_article_BBC():
        return article_template(BBC_pick_of_day, 'BBC-pick')

    @app.route('/BBC-pick-of-day-text', methods=['GET'])
    def scrape_article_BBC_text():
        result = BBC_pick_of_day(False)
        return jsonify(result)
    
    @app.route('/NPR-pick-of-day', methods=['GET'])
    def scrape_article_NPR():
        return article_template(NPR_pick_of_day, 'NPR-pick')
    
    @app.route('/NPR-pick-of-day-text', methods=['GET'])
    def scrape_article_NPR_text():
        result = NPR_pick_of_day(False)
        return jsonify(result)