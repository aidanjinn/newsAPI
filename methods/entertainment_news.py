from methods.scraping_template import scrape_template


def rolling_stone_pick_of_day(ai, language = "English"):
    url = "https://www.rollingstone.com/tv-movies/"
    attr_id = {
        'class': 'featured-stories__primary // u-flex-71p@desktop lrv-u-margin-b-2 lrv-u-margin-b-00@desktop lrv-u-align-items-center u-margin-lr-n12@mobile-max'
    }
    attr_author = {
        'class' : 'author-name // lrv-u-text-align-center lrv-u-text-transform-capitalize lrv-a-font-basic-m u-letter-spacing-003 lrv-u-margin-tb-00 lrv-u-color-black lrv-u-color-black:hover u-font-weight-800'
    }
    return scrape_template(ai, language, url, 'div', attr_id, 'p', attr_author, ['a'])

def people_pick_of_day(ai, language = "English"):
    url = "https://people.com/"
    attr_id = {'id': 'top-stories_1-0', 'class': 'comp top-stories four-post mntl-block',
                                            'data-tracking-id': 'Homepage | Top Stories',
                                            'data-tracking-container': 'true'}

    attr_author = {
        'id' : 'mntl-bylines__item_1-0'
    }
    return scrape_template(ai, language, url, 'section', attr_id, 'div', attr_author, ['a'])