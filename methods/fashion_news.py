from methods.scraping_template import scrape_template

def vogue_pick_of_day(ai, language = "English"):
    url = "https://www.vogue.com/fashion"
    attr_id = {
        'data-section-title': 'top stories collage/center'
    }
    #No author section given
    return scrape_template(ai, language, url, 'div', attr_id)

def cosmo_style(ai, language = "English"):
    url = "https://www.cosmopolitan.com/style-beauty/fashion/"
    attr_id = {
            'data-theme-key': 'big-story-feed-block-container', 'class': 'css-wgm1ip eq9yxe32'}
    attr_author = {
        'class' : 'css-19xqvq e1f1sunr5'
    }

    return scrape_template(ai, language, url, 'div', attr_id, 'div', attr_author,  ['a'])