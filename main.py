from dotenv import load_dotenv
from news import News
from stocks import Stocks
from sms import SMS
load_dotenv()


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

news1 = News(COMPANY_NAME)
stock1 = Stocks(STOCK_NAME)
sms1 = SMS()


growth_dict = stock1.check_stock_growth()

if growth_dict["growth"] == "up":
    news_list = news1.get_news_articles()
    msg = growth_dict["msg"] + f"\nLatest news:- {news_list}"
    sms1.send_text(msg)

elif growth_dict["growth"] == "down":
    news_list = news1.get_news_articles()
    msg = growth_dict["msg"] + f"\nLatest news:- {news_list}"
    sms1.send_text(msg)