from methods import tech_news
from methods.tech_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

async def fetch_tech_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(article_template,techcrunch_pick_of_day,'techcrunch-pick'),
        fetch_article(article_template,zdnet_pick_of_day, 'zdnet-pick'),
        fetch_article(article_template,wired_pick_of_day, 'wired-pick'),
        fetch_article(article_template,techreport_pick_of_day, 'techreport-pick'),
        fetch_article(article_template,infoq_pick_of_day, 'infoq-pick')
    ]
    return await asyncio.gather(*tasks)

def tech_news_register_routes(app):
    @app.route('/wired-pick-of-day', methods=['GET'])
    def scrape_article_wired():
        return article_template(wired_pick_of_day, 'wired-pick')

    @app.route('/wired-pick-of-day-text', methods=['GET'])
    def scrape_article_wired_text():
        result = wired_pick_of_day(False)
        return jsonify(result)

    @app.route('/techcrunch-pick-of-day', methods=['GET'])
    def scrape_article_techcrunch():
        return article_template(techcrunch_pick_of_day, 'techcrunch-pick')

    @app.route('/techcrunch-pick-of-day-text', methods=['GET'])
    def scrape_article_techcrunch_text():
        result = techcrunch_pick_of_day(False)
        return jsonify(result)

    @app.route('/zdnet-pick-of-day', methods=['GET'])
    def scrape_article_zdnet():
        return article_template(zdnet_pick_of_day, 'zdnet-pick')
    
    @app.route('/zdnet-pick-of-day-text', methods=['GET'])
    def scrape_article_zdnet_text():
        result = zdnet_pick_of_day(False)
        return jsonify(result)
    
    @app.route('/techreport-pick-of-day', methods=['GET'])
    def scrape_article_techreport():
        return article_template(techreport_pick_of_day, 'techreport-pick')
    
    @app.route('/techreport-pick-of-day-text', methods=['GET'])
    def scrape_article_techreport_text():
        result = techreport_pick_of_day(False)
        return jsonify(result)
    
    @app.route('/infoq-pick-of-day', methods=['GET'])
    def scrape_article_developer_tech():
        return article_template(infoq_pick_of_day, 'infoq-pick')
    
    @app.route('/infoq-pick-of-day-text', methods=['GET'])
    def scrape_article_developer_tech_text():
        result = infoq_pick_of_day(False)
        return jsonify(result)
        
    @app.route('/tech-news', methods=['GET'])
    def scrape_article_tech_news():
        return multi_template(fetch_tech_news, 'tech-news')

    @app.route('/tech-news-text', methods=['GET'])
    def scrape_article_tech_news_text():
        return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False), techreport_pick_of_day(False), infoq_pick_of_day(False)])
