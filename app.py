from flask import Flask, jsonify, request
from scraping_methods import *
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


@app.route('/wired-pick-of-day', methods=['GET'])
def scrape_article():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = wired_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = AP_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = vogue_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = rolling_stone_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = yahoo_sports_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Fetch breaking news and pick of the day in the specified language
        breaking_news = yahoo_sports_breaking_news(True, language)
        pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/", True, language)

        # Combine results, include breaking news only if it's available
        result = [breaking_news, pick_of_day] if breaking_news else [pick_of_day]

        return jsonify(result)
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
        #"https://sports.yahoo.com/soccer/",
        # "https://sports.yahoo.com/tennis/",
        # "https://sports.yahoo.com/golf/"
    ]

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = []
        for url in urls:
            result.append(yahoo_sports_pick_of_day(url, True, language))

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/yahoo-sports-recap-text', methods = ['GET'])
def scrape_article8_text():

    urls = [
        "https://sports.yahoo.com/nfl/",
        "https://sports.yahoo.com/college-football/",
        "https://sports.yahoo.com/nba/",
        "https://sports.yahoo.com/nhl/",
        "https://sports.yahoo.com/college-basketball/",
        "https://sports.yahoo.com/college-womens-basketball/",
        "https://sports.yahoo.com/mlb/",
        "https://sports.yahoo.com/soccer/",
        "https://sports.yahoo.com/tennis/",
        "https://sports.yahoo.com/golf/"
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = democracy_now_pick_of_day(True, language)

        if result:
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
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [AP_pick_of_day(True, language), democracy_now_pick_of_day(True, language), SCMP_pick_of_day(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/world-news-text', methods=['GET'])
def scape_article10_text():

    return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False)])

@app.route('/SCMP-pick-of-day', methods=['GET'])
def scape_article11():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = SCMP_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = SCMP_china(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = cosmo_style(True, language)

        if result:
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
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [vogue_pick_of_day(True, language), cosmo_style(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fashion-news-text', methods=['GET'])
def scape_article14_text():

    return jsonify([vogue_pick_of_day(False), cosmo_style(False)])

@app.route('/techcrunch-pick-of-day', methods=['GET'])
def scape_article15():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = techcrunch_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = zdnet_pick_of_day(True, language)

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/zdnet-pick-of-day-text', methods=['GET'])
def scape_article16_text():

    result = zdnet_pick_of_day(False)

    return jsonify(result)

@app.route('/tech-news', methods=['GET'])
def scape_article17():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [techcrunch_pick_of_day(True, language), zdnet_pick_of_day(True, language), wired_pick_of_day(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/tech-news-text', methods=['GET'])
def scape_article17_text():

    return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False)])

@app.route('/weather-channel-pick-of-day', methods=['GET'])
def scape_article18():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = weather_channel_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = weather_gov_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [weather_channel_pick_of_day(True, language),weather_gov_pick_of_day(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/weather-news-text', methods=['GET'])
def scape_article20_text():

    return jsonify([weather_channel_pick_of_day(False),weather_gov_pick_of_day(False)])

@app.route('/yahoo-finance-pick-of-day', methods=['GET'])
def scape_article21():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = yahoo_finance_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = economist_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = forbes_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [yahoo_finance_pick_of_day(True, language), economist_pick_of_day(True, language), forbes_pick_of_day(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/finance-news-text', methods=['GET'])
def scape_article24_text():

    return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False)])

@app.route('/people-pick-of-day', methods=['GET'])
def scape_article25():

    try:
        # Get the language query parameter, default to 'english'
        language = request.args.get('language', default='english').lower()

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = people_pick_of_day(True, language)

        if result:
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

        if language not in supported_languages:
            return jsonify({"error": f"Language '{language}' is not supported."}), 400

        # Default Behavior is AI-SUM ON; ENGLISH
        result = [rolling_stone_pick_of_day(True, language), people_pick_of_day(True, language)]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No result found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
