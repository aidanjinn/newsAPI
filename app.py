from flask import Flask, jsonify
from scraping_methods import *

'''
[JSON Object Fields]
@ Website Link:
@ Summary:
'''

app = Flask(__name__)

@app.route('/wired-pick-of-day', methods=['GET'])
def scrape_article():
    # Call the scraping function
    result = wired_pick_of_day(True)
    # Return the result as a JSON response
    return jsonify(result)

@app.route('/wired-pick-of-day-text', methods=['GET'])
def scrape_article_text():

    result = wired_pick_of_day(False)

    return jsonify(result)

@app.route('/AP-pick-of-day', methods=['GET'])
def scape_article2():

    result = AP_pick_of_day(True)

    return jsonify(result)

@app.route('/AP-pick-of-day-text', methods=['GET'])
def scrape_article2_text():

    result = AP_pick_of_day(False)

    return jsonify(result)

@app.route('/vogue-pick-of-day', methods=['GET'])
def scape_article3():

    result = vogue_pick_of_day(True)

    return jsonify(result)

@app.route('/vogue-pick-of-day-text', methods=['GET'])
def scape_article3_text():

    result = vogue_pick_of_day(False)

    return jsonify(result)

@app.route('/rolling-stone-movies-tv-pick-of-day', methods=['GET'])
def scape_article4():

    result = rolling_stone_pick_of_day(True)

    return jsonify(result)

@app.route('/rolling-stone-movies-tv-pick-of-day-text', methods=['GET'])
def scape_article4_text():

    result = rolling_stone_pick_of_day(False)

    return jsonify(result)

@app.route('/yahoo-sports-pick-of-day', methods=['GET'])
def scape_article5():

    result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", True)

    return jsonify(result)

@app.route('/yahoo-sports-pick-of-day-text', methods=['GET'])
def scape_article5_text():

    result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", False)

    return jsonify(result)

@app.route('/yahoo-sports-breaking-news', methods=['GET'])
def scape_article6():

    result = yahoo_sports_breaking_news(True)

    return jsonify(result)

@app.route('/yahoo-sports-breaking-news-text', methods=['GET'])
def scape_article6_text():

    result = yahoo_sports_breaking_news(False)

    return jsonify(result)

@app.route('/yahoo-sports', methods=['GET'])
def scape_article7():

    breaking_news = yahoo_sports_breaking_news(True)
    pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/",True)

    if breaking_news:
        result = [breaking_news, pick_of_day]
    else:
        result = [pick_of_day]

    return jsonify(result)

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

    result = []
    for url in urls:
        result.append(yahoo_sports_pick_of_day(url,True))

    return jsonify(result)


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

    result = democracy_now_pick_of_day(True)

    return jsonify(result)

@app.route('/democracy-now-pick-of-day-text', methods=['GET'])
def scape_article9_text():

    result = democracy_now_pick_of_day(False)

    return jsonify(result)

@app.route('/world-news', methods=['GET'])
def scape_article10():

    return jsonify([AP_pick_of_day(True), democracy_now_pick_of_day(True), SCMP_pick_of_day(True)])

@app.route('/world-news-text', methods=['GET'])
def scape_article10_text():

    return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False)])

@app.route('/SCMP-pick-of-day', methods=['GET'])
def scape_article11():

    result = SCMP_pick_of_day(True)

    return jsonify(result)

@app.route('/SCMP-pick-of-day-text', methods=['GET'])
def scape_article11_text():

    result = SCMP_pick_of_day(False)

    return jsonify(result)

@app.route('/SCMP-china-top-story', methods=['GET'])
def scape_article12():

    result = SCMP_china(True)

    return jsonify(result)

@app.route('/SCMP-china-top-story-text', methods=['GET'])
def scape_article12_text():

    result = SCMP_china(False)

    return jsonify(result)


@app.route('/cosmo-style-pick-of-day', methods=['GET'])
def scape_article13():

    result = cosmo_style(True)

    return jsonify(result)

@app.route('/cosmo-style-pick-of-day-text', methods=['GET'])
def scape_article13_text():

    result = cosmo_style(False)

    return jsonify(result)

@app.route('/fashion-news', methods=['GET'])
def scape_article14():

    return jsonify([vogue_pick_of_day(True), cosmo_style(True)])

@app.route('/fashion-news-text', methods=['GET'])
def scape_article14_text():

    return jsonify([vogue_pick_of_day(False), cosmo_style(False)])

@app.route('/techcrunch-pick-of-day', methods=['GET'])
def scape_article15():

    result = techcrunch_pick_of_day(True)

    return jsonify(result)

@app.route('/techcrunch-pick-of-day-text', methods=['GET'])
def scape_article15_text():

    result = techcrunch_pick_of_day(False)

    return jsonify(result)

@app.route('/zdnet-pick-of-day', methods=['GET'])
def scape_article16():

    result = zdnet_pick_of_day(True)

    return jsonify(result)

@app.route('/zdnet-pick-of-day-text', methods=['GET'])
def scape_article16_text():

    result = zdnet_pick_of_day(False)

    return jsonify(result)

@app.route('/tech-news', methods=['GET'])
def scape_article17():

    return jsonify([techcrunch_pick_of_day(True), zdnet_pick_of_day(True), wired_pick_of_day(True)])

@app.route('/tech-news-text', methods=['GET'])
def scape_article17_text():

    return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False)])

@app.route('/weather-channel-pick-of-day', methods=['GET'])
def scape_article18():

    result = weather_channel_pick_of_day(True)

    return jsonify(result)

@app.route('/weather-channel-pick-of-day-text', methods=['GET'])
def scape_article18_text():

    result = weather_channel_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-gov-pick-of-day', methods=['GET'])
def scape_article19():

    result = weather_gov_pick_of_day(True)

    return jsonify(result)

@app.route('/weather-gov-pick-of-day-text', methods=['GET'])
def scape_article19_text():

    result = weather_gov_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-news', methods=['GET'])
def scape_article20():

    return jsonify([weather_channel_pick_of_day(True),weather_gov_pick_of_day(True)])

@app.route('/weather-news-text', methods=['GET'])
def scape_article20_text():

    return jsonify([weather_channel_pick_of_day(False),weather_gov_pick_of_day(False)])

@app.route('/yahoo-finance-pick-of-day', methods=['GET'])
def scape_article21():

    result = yahoo_finance_pick_of_day(True)

    return jsonify(result)

@app.route('/yahoo-finance-pick-of-day-text', methods=['GET'])
def scape_article21_text():

    result = yahoo_finance_pick_of_day(False)

    return jsonify(result)

@app.route('/economist-pick-of-day', methods=['GET'])
def scape_article22():

    result = economist_pick_of_day(True)

    return jsonify(result)

@app.route('/economist-pick-of-day-text', methods=['GET'])
def scape_article22_text():

    result = economist_pick_of_day(False)

    return jsonify(result)

@app.route('/forbes-pick-of-day', methods=['GET'])
def scape_article23():

    result = forbes_pick_of_day(True)

    return jsonify(result)

@app.route('/forbes-pick-of-day-text', methods=['GET'])
def scape_article23_text():

    result = forbes_pick_of_day(False)

    return jsonify(result)

@app.route('/finance-news', methods=['GET'])
def scape_article24():

    return jsonify([yahoo_finance_pick_of_day(True), economist_pick_of_day(True), forbes_pick_of_day(True)])

@app.route('/finance-news-text', methods=['GET'])
def scape_article24_text():

    return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False)])

@app.route('/people-pick-of-day', methods=['GET'])
def scape_article25():

    result = people_pick_of_day(True)

    return jsonify(result)

@app.route('/people-pick-of-day-text', methods=['GET'])
def scape_article25_text():

    result = people_pick_of_day(False)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
