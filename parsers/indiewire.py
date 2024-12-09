import requests
import os
from datetime import datetime, timedelta
import pytz 

from dateutil import parser 
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from dotenv import load_dotenv

VARIETY_PARSE_URL = "https://www.indiewire.com/c/news/general-news/"

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")

async def fetch_articles(bot):
    try:
        response = requests.get(VARIETY_PARSE_URL)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        fresh_news = []
        articles = soup.find_all('div', attrs={"data-alias" : "card__main"})
        for article in articles:
            title = article.find('div', attrs={"data-alias" : "card__card-title"})
            headline = title.find('a')
            time = article.find('time',attrs={"data-alias" : "card_timestamp"})
          
            if time is not None:
                timeValue = time['datetime']
                kiev_tz = pytz.timezone("Europe/Kiev")
                pattern_datetime = datetime.strptime(timeValue, '%Y-%m-%d %H:%M:%S.%f%z').astimezone(kiev_tz)
                current_datetime = datetime.now(kiev_tz)

                time_difference = (current_datetime - pattern_datetime).total_seconds()  / 3600 # one hour check

                if time_difference < 1:
                    text = headline.get_text(strip=True)
                    translated = GoogleTranslator(source='en', target='ukrainian').translate(text=text)
                    message = f"🔹 Original: {text}\n\nПереклад: {translated}\n\n{headline['href']}"
                    fresh_news.append(message)

        if fresh_news:
            for news_item in fresh_news:
                await bot.send_message(chat_id=CHAT_ID, text=news_item)
        else:
            print("No fresh news at the moment.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

