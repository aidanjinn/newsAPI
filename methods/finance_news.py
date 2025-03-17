from methods.scraping_template import scrape_template

def yahoo_finance_pick_of_day(ai, language = "English"):
    url = "https://finance.yahoo.com/"
    attr_id = {
        'class': 'tw-border-none tw-p-0'
    }
    attr_author = {
        'class' : 'byline-attr yf-1k5w6kz'
    }
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author, ['div'])


def economist_pick_of_day(ai, language = "English"):
    url = "https://www.economist.com/"
    attr_id = {
            'id': 'new-relic-top-stories'
    }
    # not seeing authors listed for economists articles
    return scrape_template(ai, language, url, 'section', attr_id)


def forbes_pick_of_day(ai, language = "English"):
    url = "https://www.forbes.com/"
    attr_id = {
        'class': 'card card--large csf-block' 
    }
    attr_author = {
        'class' : 'ujvJmzbB LfmqX'
    }
    return scrape_template(ai, language, url,'div', attr_id, 'p', attr_author, ['a'])

def investopedia_pick_of_day(ai, language = "English"):
    url = "https://www.investopedia.com/"
    attr_id = {
        'id' : 'home-hero--news_1-0' , 'class' : 'comp home-hero--news mntl-block'
    }
    attr_author = {
        'id' : 'mntl-bylines__item_1-0'
    }
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author, ['a'])
