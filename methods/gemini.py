from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api = os.getenv('API_KEY')
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_article_with_gemini(article_text, language, title):
    prompt = (
        f"(This is the first section of the prompt: Follow it and only response with the requested information)"
        f"Summarize the following article into its main 5 points. Be concise and create the summary/points based on only the data "
        f"provided to you. Do not make up any information. Do not start your response with a response to my prompt. "
        f"Only give the summary. For format, please indicate the start of a new point using a bullet. If there is any extra information"
        f"about advertisement, donations to the publication, or information about the news site itself that does not pertain to the story, please do not include it in the summary."
        f"(Return the summary in the language: {language}, do not respond to this in response):\n\n{article_text}"
        
        f"(This is the second section of the prompt: Follow it and only response with the requested information)"
        f"\n\nAfter the summary, add exactly two newlines, then ':?PROMPT:', then a space, then list exactly 5 relevant tag words the tag words should be in {language}"
        f"separated by commas for the information within the text."
        
        f"(This is the Third section of the prompt: Follow it and only response with the requested information)"
        f"After the tags Section, add two newlines, then ':?PROMPT:', and then return this title: {title} translated to be in this language: {language} "
    )
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"
