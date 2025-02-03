import requests
from bs4 import BeautifulSoup
from methods.gemini import summarize_article_with_gemini


def rolling_stone_pick_of_day(ai, language = "English"):
    url = "https://www.rollingstone.com/tv-movies/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': 'featured-stories__primary // u-flex-71p@desktop lrv-u-margin-b-2 lrv-u-margin-b-00@desktop lrv-u-align-items-center u-margin-lr-n12@mobile-max'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.rollingstone.com' + article_link

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
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found on the Rolling Stone Movies-TV homepage."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def people_pick_of_day(ai, language = "English"):
    url = "https://people.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('section',
                                     attrs={'id': 'top-stories_1-0', 'class': 'comp top-stories four-post mntl-block',
                                            'data-tracking-id': 'Homepage | Top Stories',
                                            'data-tracking-container': 'true'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://people.com' + article_link

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
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}