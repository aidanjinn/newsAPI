from methods.entertainment_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

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
    def scape_article_rolling_stone():
        return article_template(rolling_stone_pick_of_day, 'rolling-stone-movies-tv-pick')

    @app.route('/rolling-stone-movies-tv-pick-of-day-text', methods=['GET'])
    def scape_article4_text():
        result = rolling_stone_pick_of_day(False)
        return jsonify(result)

    @app.route('/people-pick-of-day', methods=['GET'])
    def scape_article_people():
        return article_template(people_pick_of_day, 'people-pick')

    @app.route('/people-pick-of-day-text', methods=['GET'])
    def scape_article25_text():
        result = people_pick_of_day(False)
        return jsonify(result)

    @app.route('/entertainment-news', methods=['GET'])
    def scape_article_entertainment():
        return multi_article_template(fetch_entertainment_news, 'entertainment-news')

    @app.route('/entertainment-news-text', methods=['GET'])
    def scape_article26_text():
        return jsonify([rolling_stone_pick_of_day(False), people_pick_of_day(False)])
