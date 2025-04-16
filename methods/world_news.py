from methods.scraping_template import scrape_template

def AP_pick_of_day(ai, language = "English"):
    url = "https://apnews.com/"
    
    attr_id = {
        'class': 'Page-content An_Home pageMainContent'
    }
    
    attr_author = {
        'class' : 'Page-authors'
    }
    
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author, ['a', 'span'])

def democracy_now_pick_of_day(ai, language = "English"):
    url = "https://www.democracynow.org"
    attr_id = {
        'class': 'col-lg-6 col-sm-5 col-sm-pull-4', 'id': 'highlighted_stories'
    }
    
    attr_author = {
        'id' : 'guests_sm_screen'
    }
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author)

def SCMP_pick_of_day(ai, language = "English"):
    url = "https://www.scmp.com"
    attr_id = {
            'data-qa': 'HomePage-Container', 'class': 'css-1tovb67 e7j48fa38'
    }
    
    attr_author = {
        'data-qa' : 'GenericArticle-Author'
    }
    
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author)


# Chinese New Publication
def SCMP_china(ai, language = "English"):
    url = "https://www.scmp.com/news/china"
    attr_id = {
            'data-qa': 'DefaultSection-HeroArticles', 'class': 'css-lowk9u e1z0qi5433'
    }
    
    attr_author = {
        'data-qa' : 'GenericArticle-Author'
    }
    
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author)


def BBC_pick_of_day(ai, language = "English"):
    url = "https://www.bbc.com/"
    attr_id = {
        'class' : 'sc-78618877-6 oUiRD'
    }
    
    attr_author = {
        'data-testid' : 'byline-new-contributors'
    }
    
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author, ['span'])

def NPR_pick_of_day(ai, language = "English"):
    url = "https://www.npr.org/"
    
    attr_id = {
        'id' :'main-section'
    }
    
    attr_author = {
        'class' : 'byline__name byline__name--block'
    }
    
    return scrape_template(ai, language, url, 'section', attr_id, 'p', attr_author)

def japan_times_pick_of_day(ai, language = "English"):
    url = "https://www.japantimes.co.jp/"
    
    attr_id = {
        'class' : 'jt-tab-breaking-news'
    }
    
    attr_author = {
        'class' : 'byline'
    }
    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author)