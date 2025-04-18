import requests
from bs4 import BeautifulSoup
from methods.gemini import summarize_article_with_gemini

def authors_scrape(soup, div_type, attrs_id, elements):
    try:  
        authors_div = soup.find(div_type, attrs=attrs_id)
        if authors_div:
            
            
            author_list = authors_div.find(elements)
            author_names = [author.get_text(strip=True) for author in author_list if author.get_text(strip=True)]

            return ", ".join([name for name in author_names if name])
        else:
            return None
        
    except Exception as e:
        print(f"Error in authors_scrape: {e}")
        return None

def scrape_template(ai, language, url, div_type, attrs_id, author_div_type = "", author_attrs_id = "", elements=['a']):
    try:
        # Define the headers
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        }

        # Send a GET request to the AP homepage
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div with the identified class
        main_content_div = soup.find(div_type, attrs=attrs_id)

        if main_content_div:
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    base_url = url.split('/')[0] + '//' + url.split('/')[2]  # Gets https://domain.com
                    article_link = base_url + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link, headers = headers)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Looking for authors
                authors = ""
                if author_div_type != "" and author_attrs_id != "":
                    authors = authors_scrape(article_soup, author_div_type, author_attrs_id, elements)

                # Article title look for first <h1> tag
                title_comp = article_soup.find('h1')
                title = title_comp.get_text(strip=True)

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text, language, title)
                    summary, tags, title = summary.split(":?PROMPT:")
                else:
                    summary = article_text
                    tags = ""

                return {
                    "article_link": article_link,
                    "article_authors": authors,
                    "article_tags": tags,
                    "article_title": title,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return {"error": "Main content div not found on the Rolling Stone Movies-TV homepage."}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}
    
def yahoo_scrape_template(ai, language, url, div_type, attrs_id, author_div_type = "", author_attrs_id = "", elements=['a']):
    
    try:
        # Send a GET request to the AP homepage
        response = requests.get(url)
        response.raise_for_status()  

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        main_content_div = soup.find('div', attrs=attrs_id)


        if main_content_div:
  
            # Now, find the first article or link within this div
            main_article_link = main_content_div.find('a', href=True)

            if main_article_link:
                article_link = main_article_link['href']

                # Handle relative URLs by adding the base URL
                if article_link.startswith('/'):
                    base_url = url.split('/')[0] + '//' + url.split('/')[2]  # Gets https://domain.com
                    article_link = base_url + article_link

                # Send a GET request to the article page to extract the article text
                article_response = requests.get(article_link)
                article_response.raise_for_status()

                # Parse the article page
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Looking for authors
                authors = ""
                if author_div_type != "" and author_attrs_id != "":
                    authors = authors_scrape(article_soup, author_div_type, author_attrs_id, elements)

                title = article_soup.find('h1').get_text(strip=True)
                div_comp = article_soup.find('div', attrs={'class': 'caas-title-wrapper'})

                # Extract article content (usually inside <p> tags)
                paragraphs = article_soup.find_all('p')

                # Join all paragraphs to get the full article text
                article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])

                if ai:
                    summary = summarize_article_with_gemini(article_text, language, title)
                    summary, tags, title = summary.split(":?PROMPT:")
                else:
                    summary = article_text
                    tags = ""

                return {
                    "article_link": article_link,
                    "article_author" : authors,
                    "article_tags": tags,
                    "article_title": title,
                    "article_text": summary
                }
            else:
                return {"error": "No article link found in the main content div."}
        else:
            return None

    except requests.exceptions.RequestException as e:
        return None