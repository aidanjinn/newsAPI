from methods.finance_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

async def fetch_finance_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    tasks = [
        fetch_article(yahoo_finance_pick_of_day, True, language),
        fetch_article(economist_pick_of_day, True, language),
        fetch_article(forbes_pick_of_day, True, language),
        fetch_article(investopedia_pick_of_day, True, language)
    ]
    return await asyncio.gather(*tasks)

def finance_news_register_routes(app):
    
    @app.route('/yahoo-finance-pick-of-day', methods=['GET'])
    def scrape_article_yahoo_finance():
        return article_template(yahoo_finance_pick_of_day, 'yahoo-finance-pick')

    @app.route('/yahoo-finance-pick-of-day-text', methods=['GET'])
    def scrape_article_yahoo_finance_text():
        result = yahoo_finance_pick_of_day(False)
        return jsonify(result)

    @app.route('/economist-pick-of-day', methods=['GET'])
    def scrape_article_economist():
        return article_template(economist_pick_of_day, 'economist-pick')

    @app.route('/economist-pick-of-day-text', methods=['GET'])
    def scrape_article_economist_text():
        result = economist_pick_of_day(False)
        return jsonify(result)

    @app.route('/forbes-pick-of-day', methods=['GET'])
    def scrape_article_forbes():
        return article_template(forbes_pick_of_day, 'forbes-pick')

    @app.route('/forbes-pick-of-day-text', methods=['GET'])
    def scrape_article_forbes_text():
        result = forbes_pick_of_day(False)
        return jsonify(result)
    
    @app.route('/investopedia-pick-of-day')
    def scrape_article_investopedia():
        return article_template(investopedia_pick_of_day, 'investopedia-pick')
    
    @app.route('/investopedia-pick-of-day-text')
    def scrape_article_investopedia_text():
        result = investopedia_pick_of_day(False)
        return jsonify(result)

    @app.route('/finance-news', methods=['GET'])
    def scrape_article_finance_news():
        return multi_article_template(fetch_finance_news, 'finance-news')
            
    @app.route('/finance-news-text', methods=['GET'])
    def scrape_article_finance_news_text():
        return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False), investopedia_pick_of_day(False)])
