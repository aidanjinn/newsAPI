from methods.weather_news import *
from flask import jsonify, request
from methods.cache import *
from datetime import datetime
import asyncio 
from config import supported_languages
from routes.helper_functions import *

async def fetch_weather_news(language):
    async def fetch_article(func, *args):
        return await asyncio.to_thread(func, *args)
    
    tasks = [
        fetch_article(article_template, weather_channel_pick_of_day, 'weather-channel-pick'),
        fetch_article(article_template,weather_gov_pick_of_day, 'weather-gov-pick'),
    ]
    return await asyncio.gather(*tasks)

def weather_news_register_routes(app):

    @app.route('/weather-channel-pick-of-day', methods=['GET'])
    def scrape_article_weather_channel():
        return article_template(weather_channel_pick_of_day, 'weather-channel-pick')
        
    @app.route('/weather-channel-pick-of-day-text', methods=['GET'])
    def scrape_article_weather_channel_text():
        result = weather_channel_pick_of_day(False)
        return jsonify(result)

    @app.route('/weather-gov-pick-of-day', methods=['GET'])
    def scrape_article_weather_gov():
        return article_template(weather_gov_pick_of_day, 'weather-gov-pick')

    @app.route('/weather-gov-pick-of-day-text', methods=['GET'])
    def scrape_article_weather_gov_text():
        result = weather_gov_pick_of_day(False)
        return jsonify(result)

    @app.route('/weather-news', methods=['GET'])
    def scrape_article_weather_news():
        return multi_template(fetch_weather_news, 'weather-news')

    @app.route('/weather-news-text', methods=['GET'])
    def scrape_article_weather_news_text():
        return jsonify([weather_channel_pick_of_day(False),weather_gov_pick_of_day(False)])



