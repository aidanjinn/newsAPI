from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai


'''
I will later split the definitions into a different file
just have the routes here for now deal with my poor organizational skills
'''

'''
[JSON Object Fields]
@ Website Link:
@ Date:
@ Summary:
@ Authors:
'''

'''
    I know this is bad practice but the LLM will be switched out with something else
    in the future so for now my lack of security is a future problem.
'''
api = "AIzaSyApYeEExoKk12vDdglSOmLwGD7QC_HX2Bg"

'''
    This model works fine but pinging it is sometimes slow
'''
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

#
'''
    New Publication IDEAS:
        * Wikipedia Article of the Day ???
        * AP LEFT CENTER DONE 
        * NPR LEFT CENTER
        * Wired DONE
        
        * Wall Street Journal RIGHT LEANING
        * Stars and Stripes RIGHT CENTER
        
        * Pew Research Center Center
        * Weather.com
        
        * Vogue DONE FASHION
        * Cosmo
        * ESPN
    
        
        # World Block
        
        * South China Morning Post
        * DW
        
        * BBC
        * Telegraph
        * Guardian
        * Sky News
        
        * Taipei Times
        * United Daily News
        
        * Indian Express
        * Times of India
        * Hindustan Times
        
        * NHK
        
        # DEVIN LEFTIST BLOCK
        * New York Times
        * Al Jazeera Zero
        * Democracy Now
        * Grist (Climate) potential to be own category or wrapped with weather.
'''


'''
    AP: WORLD NEWS
    WIRED: TECH/WORLDS NEWS
    
    VOGUE: FASHION



'''


'''
    The General Structure of all the scraping methods are the same
    
        * Just need to find the specific div that houses the main story on the page from 
          there you simply use the soup.find and from there you can pull the <a> element that houses the href
          after that just pull the content from the <p> tag and then pass that text into the
          LLM for summary. 
          
        * RETURNS: JSON object with fields: article_link and article_text
'''
def vogue_pick_of_day(ai):
    url = "https://www.vogue.com/fashion"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={'data-section-title': 'top stories collage/center'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.vogue.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found on the Vogue homepage."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


# Function to scrape the second article from Wired's "Today’s Picks"
def wired_pick_of_day(ai):
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

            # Ensure there are enough links, and get the second one
            if len(all_links) > 1:
                second_article = all_links[1]  # Get the second link

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

                    # Extract article content (usually inside <p> tags)
                    paragraphs = article_soup.find_all('p')

                    # Join all paragraphs to get the full article text
                    article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                    if ai:
                        summary = summarize_article_with_gemini(article_text)
                    else:
                        summary = article_text

                    return {
                        "article_link": article_link,
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

# Function to scrape the front page article from AP
def AP_pick_of_day(ai):
    url = "https://apnews.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', class_='Page-content An_Home pageMainContent')

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://apnews.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found on the AP homepage."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


def rolling_stone_pick_of_day(ai):
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

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found on the Rolling Stone Movies-TV homepage."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def yahoo_sports_pick_of_day(url, ai):


    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': '_ys_m0uq4h _ys_182ob5z'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://sports.yahoo.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return None

def yahoo_sports_breaking_news(ai):
    url = "https://sports.yahoo.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': '_ys_mvhuhj'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://sports.yahoo.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return None

def democracy_now_pick_of_day(ai):
    url = "https://www.democracynow.org"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class': 'col-lg-6 col-sm-5 col-sm-pull-4', 'id': 'highlighted_stories'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.democracynow.org' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

# Chinese New Publication
def SCMP_pick_of_day(ai):
    url = "https://www.scmp.com"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'data-qa' : 'HomePage-Container', 'class' : 'css-1tovb67 e7j48fa38'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.scmp.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

# Chinese New Publication
def SCMP_china(ai):
    url = "https://www.scmp.com/news/china"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'data-qa' : 'DefaultSection-HeroArticles', 'class' : 'css-lowk9u e1z0qi5433'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.scmp.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def cosmo_style(ai):
    url = "https://www.cosmopolitan.com/style-beauty/fashion/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'data-theme-key' : 'big-story-feed-block-container', 'class' : 'css-wgm1ip eq9yxe32'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.cosmopolitan.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def techcrunch_pick_of_day(ai):
    url = "https://techcrunch.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class' : 'hero-package hero-package-2 wp-block-techcrunch-hero-package'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_content_div = main_content_div.find('h3', attrs = {'class' : 'loop-card__title'})
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://techcrunch.com/' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def zdnet_pick_of_day(ai):
    url = "https://www.zdnet.com"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class' : 'c-featureFeaturedStory'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.zdnet.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def weather_channel_pick_of_day(ai):
    url = "https://weather.com"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('main', attrs={
            'class' : 'region-main regionMain DaybreakLargeScreen--regionMain--VnUqQ', 'aria-label' : 'Main Content'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://weather.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


def weather_gov_pick_of_day(ai):
    url = "https://www.weather.gov/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class' : 'five-sixth-last'})

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
                section = article_soup.find('div', attrs= {'id' : 'printarea'})
                paragraphs = section.find_all('div', style = True)

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def yahoo_finance_pick_of_day(ai):
    url = "https://finance.yahoo.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class' : 'hero-lead yf-1m9jpnz'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://finance.yahoo.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def economist_pick_of_day(ai):
    url = "https://www.economist.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('section', attrs={
            'id' : 'new-relic-top-stories', 'class' : 'css-gbdfxv eeawncf0'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.economist.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}

def forbes_pick_of_day(ai):
    url = "https://www.forbes.com/"

    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find('div', attrs={
            'class' : 'card card--large csf-block'})

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    article_link = 'https://www.forbes.com' + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text)
                else:
                    summary = article_text

                return {
                    "article_link": article_link,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


# Function to summarize article using Gemini
def summarize_article_with_gemini(article_text):
    prompt = (f"Summarize the following article into its main 5 points be concise and create the summary/points based on only the data"
              f"provided to you. Do not make up any information only use what I give you. Do not start your response with a response to my prompt"
              f"Only Give the Summary::\n\n{article_text}")
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"



@app.route('/wired-pick-of-day', methods=['GET'])
def scrape_article():
    # Call the scraping function
    result = wired_pick_of_day(True)
    # Return the result as a JSON response
    return jsonify(result)

@app.route('/wired-pick-of-day-text', methods=['GET'])
def scrape_article_text():
    # Call the scraping function
    result = wired_pick_of_day(False)
    # Return the result as a JSON response
    return jsonify(result)

@app.route('/AP-pick-of-day', methods=['GET'])
def scape_article2():

    result = AP_pick_of_day(True)

    return jsonify(result)

@app.route('/AP-pick-of-day-text', methods=['GET'])
def scrape_article2_text():
    # Call the scraping function
    result = AP_pick_of_day(False)
    # Return the result as a JSON response
    return jsonify(result)


@app.route('/vogue-pick-of-day', methods=['GET'])
def scape_article3():

    result = vogue_pick_of_day(True)

    return jsonify(result)

@app.route('/vogue-pick-of-day-text', methods=['GET'])
def scape_article3_text():

    result = vogue_pick_of_day(False)

    return jsonify(result)

@app.route('/rolling-stone-movies-tv-pick-of-day', methods=['GET'])
def scape_article4():

    result = rolling_stone_pick_of_day(True)

    return jsonify(result)

@app.route('/rolling-stone-movies-tv-pick-of-day-text', methods=['GET'])
def scape_article4_text():

    result = rolling_stone_pick_of_day(False)

    return jsonify(result)


'''
    Yahoo Sports Section
'''
@app.route('/yahoo-sports-pick-of-day', methods=['GET'])
def scape_article5():

    result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", True)

    return jsonify(result)

@app.route('/yahoo-sports-pick-of-day-text', methods=['GET'])
def scape_article5_text():

    result = yahoo_sports_pick_of_day("https://sports.yahoo.com/", False)

    return jsonify(result)

@app.route('/yahoo-sports-breaking-news', methods=['GET'])
def scape_article6():

    result = yahoo_sports_breaking_news(True)

    return jsonify(result)

@app.route('/yahoo-sports-breaking-news-text', methods=['GET'])
def scape_article6_text():

    result = yahoo_sports_breaking_news(False)

    return jsonify(result)

@app.route('/yahoo-sports', methods=['GET'])
def scape_article7():

    breaking_news = yahoo_sports_breaking_news(True)
    pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/",True)

    if breaking_news:
        result = [breaking_news, pick_of_day]
    else:
        result = [pick_of_day]

    return jsonify(result)

@app.route('/yahoo-sports-text', methods=['GET'])
def scape_article7_text():

    breaking_news = yahoo_sports_breaking_news(False)
    pick_of_day = yahoo_sports_pick_of_day("https://sports.yahoo.com/",False)

    if breaking_news:
        result = [breaking_news, pick_of_day]
    else:
        result = [pick_of_day]

    return jsonify(result)


@app.route('/yahoo-sports-recap', methods = ['GET'])
def scrape_article8():

    urls = [
        "https://sports.yahoo.com/nfl/",
        "https://sports.yahoo.com/college-football/",
        "https://sports.yahoo.com/nba/",
        "https://sports.yahoo.com/nhl/",
        "https://sports.yahoo.com/college-basketball/",
        "https://sports.yahoo.com/college-womens-basketball/",
        "https://sports.yahoo.com/mlb/"
    ]

    result = []
    for url in urls:
        result.append(yahoo_sports_pick_of_day(url,True))

    return jsonify(result)


@app.route('/yahoo-sports-recap-text', methods = ['GET'])
def scrape_article8_text():

    urls = [
        "https://sports.yahoo.com/nfl/",
        "https://sports.yahoo.com/college-football/",
        "https://sports.yahoo.com/nba/",
        "https://sports.yahoo.com/nhl/",
        "https://sports.yahoo.com/college-basketball/",
        "https://sports.yahoo.com/college-womens-basketball/",
        "https://sports.yahoo.com/mlb/"
    ]

    result = []
    for url in urls:
        result.append(yahoo_sports_pick_of_day(url,False))

    return jsonify(result)

'''
    Yahoo Sports Section Done
'''

@app.route('/democracy-now-pick-of-day', methods=['GET'])
def scape_article9():

    result = democracy_now_pick_of_day(True)

    return jsonify(result)

@app.route('/democracy-now-pick-of-day-text', methods=['GET'])
def scape_article9_text():

    result = democracy_now_pick_of_day(False)

    return jsonify(result)

@app.route('/world-news', methods=['GET'])
def scape_article10():

    return jsonify([AP_pick_of_day(True), democracy_now_pick_of_day(True), SCMP_pick_of_day(True)])

@app.route('/world-news-text', methods=['GET'])
def scape_article10_text():

    return jsonify([AP_pick_of_day(False), democracy_now_pick_of_day(False), SCMP_pick_of_day(False)])

@app.route('/SCMP-pick-of-day', methods=['GET'])
def scape_article11():

    result = SCMP_pick_of_day(True)

    return jsonify(result)

@app.route('/SCMP-pick-of-day-text', methods=['GET'])
def scape_article11_text():

    result = SCMP_pick_of_day(False)

    return jsonify(result)

@app.route('/SCMP-china-top-story', methods=['GET'])
def scape_article12():

    result = SCMP_china(True)

    return jsonify(result)

@app.route('/SCMP-china-top-story-text', methods=['GET'])
def scape_article12_text():

    result = SCMP_china(False)

    return jsonify(result)


@app.route('/cosmo-style-pick-of-day', methods=['GET'])
def scape_article13():

    result = cosmo_style(True)

    return jsonify(result)

@app.route('/cosmo-style-pick-of-day-text', methods=['GET'])
def scape_article13_text():

    result = cosmo_style(False)

    return jsonify(result)

@app.route('/fashion-news', methods=['GET'])
def scape_article14():

    return jsonify([vogue_pick_of_day(True), cosmo_style(True)])

@app.route('/fashion-news-text', methods=['GET'])
def scape_article14_text():

    return jsonify([vogue_pick_of_day(False), cosmo_style(False)])

@app.route('/techcrunch-pick-of-day', methods=['GET'])
def scape_article15():

    result = techcrunch_pick_of_day(True)

    return jsonify(result)

@app.route('/techcrunch-pick-of-day-text', methods=['GET'])
def scape_article15_text():

    result = techcrunch_pick_of_day(False)

    return jsonify(result)

@app.route('/zdnet-pick-of-day', methods=['GET'])
def scape_article16():

    result = zdnet_pick_of_day(True)

    return jsonify(result)

@app.route('/zdnet-pick-of-day-text', methods=['GET'])
def scape_article16_text():

    result = zdnet_pick_of_day(False)

    return jsonify(result)

@app.route('/tech-news', methods=['GET'])
def scape_article17():

    return jsonify([techcrunch_pick_of_day(True), zdnet_pick_of_day(True), wired_pick_of_day(True)])

@app.route('/tech-news-text', methods=['GET'])
def scape_article17_text():

    return jsonify([techcrunch_pick_of_day(False), zdnet_pick_of_day(False), wired_pick_of_day(False)])

@app.route('/weather-channel-pick-of-day', methods=['GET'])
def scape_article18():

    result = weather_channel_pick_of_day(True)

    return jsonify(result)

@app.route('/weather-channel-pick-of-day-text', methods=['GET'])
def scape_article18_text():

    result = weather_channel_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-gov-pick-of-day', methods=['GET'])
def scape_article19():

    result = weather_gov_pick_of_day(True)

    return jsonify(result)

@app.route('/weather-gov-pick-of-day-text', methods=['GET'])
def scape_article19_text():

    result = weather_gov_pick_of_day(False)

    return jsonify(result)

@app.route('/weather-news', methods=['GET'])
def scape_article20():

    return jsonify([weather_channel_pick_of_day(True),weather_gov_pick_of_day(True)])

@app.route('/weather-news-text', methods=['GET'])
def scape_article20_text():

    return jsonify([weather_channel_pick_of_day(False),weather_gov_pick_of_day(False)])

@app.route('/yahoo-finance-pick-of-day', methods=['GET'])
def scape_article21():

    result = yahoo_finance_pick_of_day(True)

    return jsonify(result)

@app.route('/yahoo-finance-pick-of-day-text', methods=['GET'])
def scape_article21_text():

    result = yahoo_finance_pick_of_day(False)

    return jsonify(result)

@app.route('/economist-pick-of-day', methods=['GET'])
def scape_article22():

    result = economist_pick_of_day(True)

    return jsonify(result)

@app.route('/economist-pick-of-day-text', methods=['GET'])
def scape_article22_text():

    result = economist_pick_of_day(False)

    return jsonify(result)

@app.route('/forbes-pick-of-day', methods=['GET'])
def scape_article23():

    result = forbes_pick_of_day(True)

    return jsonify(result)

@app.route('/forbes-pick-of-day-text', methods=['GET'])
def scape_article23_text():

    result = forbes_pick_of_day(False)

    return jsonify(result)

@app.route('/finance-news', methods=['GET'])
def scape_article24():

    return jsonify([yahoo_finance_pick_of_day(True), economist_pick_of_day(True), forbes_pick_of_day(True)])

@app.route('/finance-news-text', methods=['GET'])
def scape_article24_text():

    return jsonify([yahoo_finance_pick_of_day(False), economist_pick_of_day(False), forbes_pick_of_day(False)])

if __name__ == '__main__':
    app.run(debug=True)
