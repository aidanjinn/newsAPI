from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api = os.getenv('API_KEY')
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_article_with_gemini(article_text, language):
    prompt = (
        f"Summarize the following article into its main 5 points be concise and create the summary/points based on only the data"
        f"provided to you. Do not make up any information only use what I give you. Do not start your response with a response to my prompt"
        f"Only Give the Summary for format please indicate the start of a new point using a bullet. (In the language:{language}, do not respond to this in response)::\n\n{article_text}")
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"