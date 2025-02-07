from methods.scraping_template import scrape_template

def AP_pick_of_day(ai, language = "English"):
    url = "https://apnews.com/"
    attr_id = {
        'class': 'Page-content An_Home pageMainContent'
    }
    return scrape_template(ai, language, url,'div', attr_id)

def democracy_now_pick_of_day(ai, language = "English"):
    url = "https://www.democracynow.org"
    attr_id = {
        'class': 'col-lg-6 col-sm-5 col-sm-pull-4', 'id': 'highlighted_stories'
    }
    return scrape_template(ai, language, url, 'div', attr_id)

def SCMP_pick_of_day(ai, language = "English"):
    url = "https://www.scmp.com"
    attr_id = {
            'data-qa': 'HomePage-Container', 'class': 'css-1tovb67 e7j48fa38'
    }
    return scrape_template(ai, language, url, 'div', attr_id)


# Chinese New Publication
def SCMP_china(ai, language = "English"):
    url = "https://www.scmp.com/news/china"
    attr_id = {
            'data-qa': 'DefaultSection-HeroArticles', 'class': 'css-lowk9u e1z0qi5433'
    }
    return scrape_template(ai, language, url, 'div', attr_id)


def BBC_pick_of_day(ai, language = "English"):
    url = "https://www.bbc.com/"
    attr_id = {
        'class' : 'sc-c6f6255e-0 eGcloy'
    }
    return scrape_template(ai, language, url, 'div', attr_id)

def NPR_pick_of_day(ai, language = "English"):
    url = "https://www.npr.org/"
    attr_id = {
        'id' :'main-section'
    }
    return scrape_template(ai, language, url, 'section', attr_id)

def japan_times_pick_of_day(ai, language = "English"):
    url = "https://www.japantimes.co.jp/"
    attr_id = {
        'class' : 'jt-tab-breaking-news'
    }
    return scrape_template(ai, language, url, 'div', attr_id)