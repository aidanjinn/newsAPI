from methods.scraping_template import scrape_template

def yahoo_finance_pick_of_day(ai, language = "English"):
    url = "https://finance.yahoo.com/"
    attr_id = {
        'class': 'hero-lead yf-1m9jpnz'  
    }
    return scrape_template(ai, language, url, 'div', attr_id)


def economist_pick_of_day(ai, language = "English"):
    url = "https://www.economist.com/"
    attr_id = {
            'id': 'new-relic-top-stories'}
    return scrape_template(ai, language, url, 'section', attr_id)


def forbes_pick_of_day(ai, language = "English"):
    url = "https://www.forbes.com/"
    attr_id = {
        'class': 'card card--large csf-block' 
    }
    return scrape_template(ai, language, url,'div', attr_id)

def investopedia_pick_of_day(ai, language = "English"):
    url = "https://www.investopedia.com/"
    attr_id = {
        'id' : 'home-hero--news_1-0' , 'class' : 'comp home-hero--news mntl-block'
    }
    return scrape_template(ai, language, url, 'div', attr_id)
