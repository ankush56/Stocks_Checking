import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

url = "https://www.alphavantage.co/query"

API_KEY = os.environ.get('API_KEY')
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
PERCENTAGE_CHECK = 1
##SMS settings
# account_sid = os.environ.get('account_sid')
# auth_token = os.environ.get('auth_token')
# client = Client(account_sid, auth_token)


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

#We dont know if there is previous day in weekday or holiday in between
# So we convert dict to iterator, so we can iterate with next
iterator = iter(timeseries_daily.items())
for i in range(2):
    a = next(iterator)
    days_list.append(a)


# Trim tuples in list to get yesterday and day before yesterday max
yesterday_max = float(days_list[0][1]['2. high'])
day_before_yesterday_max = float(days_list[1][1]['2. high'])

print(f"yesterday_max {yesterday_max}")
print(f"day_before_yesterday_max {day_before_yesterday_max}")

percentage_amount = (day_before_yesterday_max * PERCENTAGE_CHECK) / 100
print(f"five_percentage {percentage_amount}")

difference = day_before_yesterday_max - yesterday_max
print(f"difference {difference}")

if yesterday_max > percentage_amount + day_before_yesterday_max:
    print(f"stock went up more than {PERCENTAGE_CHECK} % percentage")

elif yesterday_max < day_before_yesterday_max - percentage_amount:
    print(f"Stock went down by {PERCENTAGE_CHECK} % percent")
else:
    print(F"Stock neither went up by {PERCENTAGE_CHECK} %,  neither dropped")






## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
# """
# TSLA: 2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

