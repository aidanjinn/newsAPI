import requests
from bs4 import BeautifulSoup
from methods.gemini import summarize_article_with_gemini
from methods.scraping_template import scrape_template

def wired_pick_of_day(ai, language = "English"):
    url = "https://www.wired.com/"

    try:
        # Send a GET request to the Wired homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with id 'today’s-picks'
        todays_picks_div = soup.find('div', id="today’s-picks")

        if todays_picks_div:
            # Find all the links in "Today’s Picks" section
            all_links = todays_picks_div.find_all('a')

            if len(all_links) > 1:
                second_article = all_links[1]

                if second_article and second_article.get('href'):
                    article_link = second_article['href']

                    # Handle relative URLs by adding the base URL
                    if article_link.startswith('/'):
                        article_link = 'https://www.wired.com' + article_link

                    # Send a GET request to the article page to extract the article text
                    article_response = requests.get(article_link)
                    article_response.raise_for_status()

                    # Parse the article page
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')

                    # Article title look for first <h1> tag
                    title_comp = article_soup.find('h1')
                    title = title_comp.get_text(strip=True)

                    # Extract article content (usually inside <p> tags)
                    paragraphs = article_soup.find_all('p')

                    # Join all paragraphs to get the full article text
                    article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                    if ai:
                        summary = summarize_article_with_gemini(article_text, language)
                    else:
                        summary = article_text

                    return {
                        "article_link": article_link,
                        "article_title": title,
                        "article_text": summary
                    }
                else:
                    return {"error": "Second link does not have an href attribute."}
            else:
                return {"error": "There are not enough links in 'today’s-picks' to fetch the second one."}
        else:
            return {"error": "No 'today’s-picks' section found on the page."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def techcrunch_pick_of_day(ai, language = "English"):
    url = "https://techcrunch.com/"

    try:
        # Send a GET request to the homepage
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': 'hero-package-2__featured'})
        main_content_div = main_content_div.find('h3', attrs={'class': 'loop-card__title'})

        if main_content_div:
            # Find the article link more directly
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://techcrunch.com' + article_link

                # Send a GET request to the article page
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                try:
                    
                    title_comp = (
                        article_soup.find('h1', {'class': 'article__title'}) or
                        article_soup.find('h1', {'class': 'article-hero__title'}) or
                        article_soup.find('h1')
                    )
                    title = title_comp.get_text(strip=True) if title_comp else "Title not found"
                except Exception:
                    title = "Title not found"

                # Extract article content
                paragraphs = article_soup.find_all('p')
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text, language)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_title": title,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


def zdnet_pick_of_day(ai, language = "English"):
    url = "https://www.zdnet.com"
    attr_id = {
        'class': 'c-featureFeaturedStory'
    }
    return scrape_template(ai, language, url, 'div', attr_id)