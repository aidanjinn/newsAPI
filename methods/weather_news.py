import requests
from bs4 import BeautifulSoup
from methods.gemini import summarize_article_with_gemini
from methods.scraping_template import scrape_template

def weather_channel_pick_of_day(ai, language = "English"):
    url = "https://weather.com"
    attr_id = {
            'class': 'region-main regionMain DaybreakLargeScreen--regionMain--VnUqQ', 'aria-label': 'Main Content'}
    
    attr_author = {
        'class' : 'ArticleHeader--header--5NFZ-'
    }
    
    return scrape_template(ai, language, url, 'main', attr_id, 'div', attr_author)


def weather_gov_pick_of_day(ai, language = "English"):
    url = "https://www.weather.gov/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': 'five-sixth-last'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.weather.gov' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                section = article_soup.find('div', attrs={'id': 'printarea'})
                paragraphs = section.find_all('div', style=True)

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text, language)
                    summary, tags = summary.split(":?TAGS:")
                else:
                    summary = article_text
                    tags = ""

                return {
                    "article_link": article_link,
                    "article_author" : "NWS Weather Prediction Center College Park MD",
                    "article_tags": tags,
                    "article_title": "Short Range Forecast Discussion",
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}