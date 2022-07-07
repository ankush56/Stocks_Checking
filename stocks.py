import requests
import os


class Stocks:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.STOCK_URL = "https://www.alphavantage.co/query"
        self.THRESHOLD_PERCENTAGE_CHECK = 0.5
        self.stocks_parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_name,
            "apikey": os.environ.get('API_KEY')
        }

    def fetch_stock_data(self):
        response = requests.get(self.STOCK_URL, self.stocks_parameters)
        response.raise_for_status()
        data = response.json()
        timeseries_daily = data['Time Series (Daily)']
        return timeseries_daily

    def calculate_percentage_diff(self, amount, difference):
        result = difference * 100 / amount
        return result

    def check_stock_growth(self):
        timeseries_daily = self.fetch_stock_data()
        days_list = []
        msg= ""

        # We don't know if there is previous day in weekday or holiday in between
        # So we convert dict to iterator, so we can iterate with next
        iterator = iter(timeseries_daily.items())
        for i in range(2):
            a = next(iterator)
            days_list.append(a)

        # Trim tuples in list to get yesterday and day before yesterday max
        yesterday_max = float(days_list[0][1]['2. high'])
        day_before_yesterday_max = float(days_list[1][1]['2. high'])

        # Check if it went up or down by threshold percentage(1%, 5%)
        # When Threshold is met only then it will send sms
        percentage_amount = (day_before_yesterday_max * self.THRESHOLD_PERCENTAGE_CHECK) / 100
        difference = day_before_yesterday_max - yesterday_max

        # Calculate How much percentage it went up by or down
        percentage_difference = self.calculate_percentage_diff(day_before_yesterday_max, difference)

        if yesterday_max > percentage_amount + day_before_yesterday_max:
            growth = "up"
            msg = f"{self.stock_name}-{percentage_difference} *UP*\nHigh-{yesterday_max}\nPrevious_Day_High-{day_before_yesterday_max}"

        elif yesterday_max < day_before_yesterday_max - percentage_amount:
            growth = "down"
            msg = f"{self.stock_name}-{percentage_difference} *DOWN*\nHigh-{yesterday_max}\nPrevious_Day_High-{day_before_yesterday_max}"

        else:
            print(F"Stock neither went up by {self.THRESHOLD_PERCENTAGE_CHECK} %,  neither dropped")

        growth_status = {}
        growth_status.update({"growth": growth, "msg": msg})
        return growth_status
