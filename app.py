from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

api = "AIzaSyApYeEExoKk12vDdglSOmLwGD7QC_HX2Bg"

#
'''
    New Publication IDEAS:
        * Wikipedia Article of the Day ???
        * AP LEFT CENTER
        * NPR LEFT CENTER
        
        * Wall Street Journal RIGHT LEANING
        * Stars and Stripes RIGHT CENTER
        
        * Pew Research Center Center
        * Weather.com
        
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


# Function to scrape the second article from Wired's "Today’s Picks"
def wired_pick_of_day():
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

                    summary = summarize_article_with_gemini(article_text)

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
def AP_pick_of_day():
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

                summary = summarize_article_with_gemini(article_text)

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


import google.generativeai as genai
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to summarize article using Gemini
def summarize_article_with_gemini(article_text):
    prompt = f"Summarize the following article into its main points:\n\n{article_text}"
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"


# Define a route to handle the web scraping API
@app.route('/wired-pick-of-day', methods=['GET'])
def scrape_article():
    # Call the scraping function
    result = wired_pick_of_day()
    # Return the result as a JSON response
    return jsonify(result)

@app.route('/AP-pick-of-day', methods=['GET'])
def scape_article2():

    result = AP_pick_of_day()
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
