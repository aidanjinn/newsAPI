from methods.scraping_template import yahoo_scrape_template

def yahoo_sports_pick_of_day(url, ai, language = "English"):
    attr_id = {
        'class': '_ys_1unhdgw _ys_1kkgpmk'
    }
    attr_author = {
        'class' : 'caas-attr-item-author'
    }
    return yahoo_scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author)

def yahoo_sports_breaking_news(ai, language = "English"):
    url = "https://sports.yahoo.com/"
    attr_id = {
            'class': '_ys_mvhuhj'
    }
    attr_author = {
        'class' : 'caas-attr-item-author'
    }
    return yahoo_scrape_template(ai, language, url, 'div', attr_id)