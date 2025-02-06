# News Summarization API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange)

The **News Summarization API** is a powerful tool built using **Python**, **Flask**, and **Google Gemini**. It provides summarized news articles from multiple publications and topics, including world news, sports, entertainment, and weather. Additionally, it supports translation of articles and summaries into most languages.

[Deployed API to ping](https://newsapi-r8fr.onrender.com/)
[Deployed Frontend](https://recap-nine.vercel.app/)

---

# Project Structure
```tree
newsAPI/
├── app.py
├── config.py
├── methods/
|   ├── cache.py
│   ├── entertainment_news.py
│   ├── fashion_news.py
│   ├── finance_news.py
│   ├── gemini.py
│   ├── sports_news.py
│   ├── tech_news.py
│   ├── weather_news.py
│   └── world_news.py
├── routes/
│   ├── entertainment_news_route.py
│   ├── fashion_news_route.py
│   ├── finance_news_route.py
│   ├── sports_news_route.py
│   ├── tech_news_route.py
│   ├── weather_news_route.py
│   └── world_news_route.py
├── templates/
│   └── index.html
└── tests/
    ├── test_routes.py
    ├── test_cache.py
    ├── test_scraping.py
    └── test_time_cache.py
```
---

## Features

- **Multi-Publication Support**: Fetch news from a variety of sources like Wired, AP, Vogue, Yahoo Sports, and more.
- **AI-Powered Summaries**: Get concise summaries of articles using Google Gemini.
- **Language Translation**: Translate articles or summaries into your preferred language.
- **Raw Article Text**: Option to retrieve the full article text without AI summarization.
- **Article Caching**: Cache summaries to improve performance.

---

## How to Use

### Hosting
You can either host the API yourself or use the deployed version. Simply make requests to the supported API routes.

### Language Translation
To translate an article or summary, append `?language=your_language` to the API endpoint. The default language is English.

**Example**:  
`/wired-pick-of-day?language=spanish` returns the Wired pick of the day in Spanish.

### Raw Article Text
If you want the full article text without an AI summary, add `-text` to the end of the API call.

**Example**:  
`/wired-pick-of-day-text` returns the full article text from Wired.

---

## Supported Routes

Below is a list of all supported API routes:

| Route                                      | Description                                      |
|--------------------------------------------|--------------------------------------------------|
| `/wired-pick-of-day`                       | Wired's pick of the day                          |
| `/AP-pick-of-day`                          | Associated Press's pick of the day               |
| `/vogue-pick-of-day`                       | Vogue's pick of the day                          |
| `/rolling-stone-movies-tv-pick-of-day`     | Rolling Stone's movies/TV pick of the day        |
| `/yahoo-sports`                            | Yahoo Sports (breaking news and pick of the day) |
| `/democracy-now-pick-of-day`               | Democracy Now's pick of the day                  |
| `/world-news`                              | Top world news stories                           |
| `/SCMP-pick-of-day`                        | South China Morning Post's pick of the day       |
| `/SCMP-china-top-story`                    | SCMP's top China story                           |
| `/cosmo-style-pick-of-day`                 | Cosmopolitan's style pick of the day             |
| `/fashion-news`                            | Latest fashion news                              |
| `/techcrunch-pick-of-day`                  | TechCrunch's pick of the day                     |
| `/zdnet-pick-of-day`                       | ZDNet's pick of the day                          |
| `/tech-news`                               | Top tech news                                    |
| `/weather-channel-pick-of-day`             | The Weather Channel's pick of the day            |
| `/weather-gov-pick-of-day`                 | Weather.gov's pick of the day                    |
| `/weather-news`                            | Latest weather news                              |
| `/yahoo-finance-pick-of-day`               | Yahoo Finance's pick of the day                  |
| `/economist-pick-of-day`                   | The Economist's pick of the day                  |
| `/forbes-pick-of-day`                      | Forbes' pick of the day                          |
| `/finance-news`                            | Top finance news                                 |
| `/yahoo-sports-recap`                      | Top articles for major sports leagues            |
| `/people-pick-of-day`                      | People's pick of the day                         |
| `/entertainment-news`                      | Latest entertainment news                        |

---

## Example Requests

1. **Get Wired's pick of the day in Spanish**:  
   `GET /wired-pick-of-day?language=spanish`

2. **Get full article text from AP**:  
   `GET /AP-pick-of-day-text`

3. **Get Yahoo Sports recap**:  
   `GET /yahoo-sports-recap`

---

## Deployment

You can deploy this API on your preferred platform (e.g., Heroku, AWS, Google Cloud). Ensure you have the required environment variables set up, including your Google Gemini API key.

---

## Contributing

Contributions are welcome! If you'd like to add new features, fix bugs, or improve documentation, please open an issue or submit a pull request.

---

Enjoy using the **News Summarization API**! For any questions or issues, feel free to open an issue on GitHub.
