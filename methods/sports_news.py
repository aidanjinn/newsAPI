from methods.scraping_template import yahoo_scrape_template

def yahoo_sports_pick_of_day(url, ai, language = "English"):
    attr_id = {
        'class': '_ys_1unhdgw _ys_1kkgpmk'
    }
    return yahoo_scrape_template(ai, language, url, 'div', attr_id)

def yahoo_sports_breaking_news(ai, language = "English"):
    url = "https://sports.yahoo.com/"
    attr_id = {
            'class': '_ys_mvhuhj'
    }
    return yahoo_scrape_template(ai, language, url, 'div', attr_id)