from methods.fashion_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

async def fetch_fashion_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(vogue_pick_of_day, True, language),
        fetch_article(cosmo_style, True, language)
    ]
    return await asyncio.gather(*tasks)

def fashion_news_register_routes(app):
    
    @app.route('/vogue-pick-of-day', methods=['GET'])
    def scrape_article_vogue():
        return article_template(vogue_pick_of_day, 'vogue-pick')
        
    @app.route('/vogue-pick-of-day-text', methods=['GET'])
    def scrape_article_vogue_text():
        result = vogue_pick_of_day(False)
        return jsonify(result)

    @app.route('/cosmo-style-pick-of-day', methods=['GET'])
    def scrape_article_cosmo():
        return article_template(cosmo_style, 'cosmo-style-pick')

    @app.route('/cosmo-style-pick-of-day-text', methods=['GET'])
    def scrape_article_cosmo_text():
        result = cosmo_style(False)
        return jsonify(result)

    @app.route('/fashion-news', methods=['GET'])
    def scrape_article_fashion():
        return multi_article_template(fetch_fashion_news, 'fashion-news')

    @app.route('/fashion-news-text', methods=['GET'])
    def scrape_article14_text():
        return jsonify([vogue_pick_of_day(False), cosmo_style(False)])
