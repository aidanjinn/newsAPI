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


def weather_gov_pick_of_day(ai, language="English"):
    url = "https://www.wpc.ncep.noaa.gov/discussions/hpcdiscussions.php?disc=pmdspd"

    try:
        # Send a GET request to the WPC short range forecast page
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.find('div', attrs={'id': 'printarea'})

        if not section:
            return {"error": "Main forecast content not found on the WPC page."}

        paragraphs = section.find_all('div', style=True)
        if not paragraphs:
            return {"error": "No paragraphs found in the forecast content section."}

        # Join all paragraphs to get the full article text
        article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

        if ai:
            try:
                summary = summarize_article_with_gemini(article_text, language, "")
                summary, tags, title = summary.split(":?PROMPT:")
            except Exception as e:
                return {"error": f"AI summarization failed: {e}"}
        else:
            summary = article_text
            tags = ""

        return {
            "article_link": url,
            "article_author": "NWS Weather Prediction Center College Park MD",
            "article_tags": tags,
            "article_title": "Short Range Forecast Discussion",
            "article_text": summary
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error occurred while fetching the WPC forecast: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


