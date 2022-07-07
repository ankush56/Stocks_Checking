import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

url = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"

API_KEY = os.environ.get('API_KEY')
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
THRESHOLD_PERCENTAGE_CHECK = 0.5

#SMS settings
account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
client = Client(account_sid, auth_token)


news_params = {
    "q": COMPANY_NAME,
    "sortBy": "publishedAt,relevancy",
    "apiKey": os.environ.get('NEWS_API_KEY'),
    "language": "en",
}

def get_news_articles():
    news_response = requests.get(NEWS_URL, news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    articles = news_data["articles"]
    articles_list = []

    for x in range(0, 3):

        tuple1 = (f"Headline- {articles[x]['title']}", f"Brief- {articles[x]['description']}", f"Link- {articles[x]['url']}")
        articles_list.append(tuple1)
    return articles_list

def send_sms(msg):
    message = client.messages \
    .create(
    body=msg,
    to=os.environ.get('dest'),
    from_='+18643839494'
    )


def calculate_percentage_diff(amount, difference):
    result = difference * 100/amount
    return result


parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY
}

response = requests.get(url, parameters)
response.raise_for_status()
data = response.json()

timeseries_daily = data['Time Series (Daily)']

days_list = []

# We don't know if there is previous day in weekday or holiday in between
# So we convert dict to iterator, so we can iterate with next

iterator = iter(timeseries_daily.items())
for i in range(2):
    a = next(iterator)
    days_list.append(a)

# Trim tuples in list to get yesterday and day before yesterday max
yesterday_max = float(days_list[0][1]['2. high'])
day_before_yesterday_max = float(days_list[1][1]['2. high'])


percentage_amount = (day_before_yesterday_max * THRESHOLD_PERCENTAGE_CHECK) / 100
difference = day_before_yesterday_max - yesterday_max
percentage_difference = calculate_percentage_diff(day_before_yesterday_max, difference)

if yesterday_max > percentage_amount + day_before_yesterday_max:
    news_list = get_news_articles()
    msg = f"{STOCK}-{percentage_difference} UP\nHigh-{yesterday_max}\nPrevious Day High {day_before_yesterday_max}\
    Latest news:- {news_list}"
    send_sms(msg)

elif yesterday_max < day_before_yesterday_max - percentage_amount:
    news_list = get_news_articles()
    msg = f"{STOCK}-{percentage_difference} Down\nLatest news:- {news_list}"
    send_sms(msg)

else:
    print(F"Stock neither went up by {THRESHOLD_PERCENTAGE_CHECK} %,  neither dropped")



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
# """
# TSLA: 2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """
