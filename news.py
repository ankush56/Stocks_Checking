import requests
import os


class News:
    def __init__(self, company_name):
        self.company_name = company_name
        self.NEWS_URL = "https://newsapi.org/v2/everything"
        self.news_params = {
            "q": self.company_name,
            "sortBy": "publishedAt,relevancy",
            "apiKey": os.environ.get('NEWS_API_KEY'),
            "language": "en",
        }

    def get_news_articles(self):
        news_response = requests.get(self.NEWS_URL, self.news_params)
        news_response.raise_for_status()
        news_data = news_response.json()

        articles = news_data["articles"]
        articles_list = []

        for x in range(0, 3):
            tuple1 = (
                f"Headline- {articles[x]['title']}", f"Brief- {articles[x]['description']}",
                f"Link- {articles[x]['url']}")
            articles_list.append(tuple1)

        return articles_list
