from methods.scraping_template import scrape_template


def rolling_stone_pick_of_day(ai, language = "English"):
    url = "https://www.rollingstone.com/tv-movies/"
    attr_id = {
        'class': 'featured-stories__primary // u-flex-71p@desktop lrv-u-margin-b-2 lrv-u-margin-b-00@desktop lrv-u-align-items-center u-margin-lr-n12@mobile-max'
    }
    return scrape_template(ai, language, url, 'div', attr_id)

def people_pick_of_day(ai, language = "English"):
    url = "https://people.com/"
    attr_id = {'id': 'top-stories_1-0', 'class': 'comp top-stories four-post mntl-block',
                                            'data-tracking-id': 'Homepage | Top Stories',
                                            'data-tracking-container': 'true'}
    
    return scrape_template(ai, language, url, 'section', attr_id)