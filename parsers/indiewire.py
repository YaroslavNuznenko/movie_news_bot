import requests
import os

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
        articles = soup.find_all('li', class_='o-tease-list__item')
        for article in articles:
            title = article.find('h3', class_='c-title')
            headline = title.find('a')
            link = article.find('a', href=True)

            time = article.find('time', class_='c-timestamp')
            timeText = time.get_text(strip=True)
            minutesValue = timeText.split(' mins')[0]

            try:
                num = int(minutesValue)  
                minutes = int(minutesValue)
                if headline and link and minutes:
                    text = headline.get_text(strip=True)
                    translated = GoogleTranslator(source='en', target='ukrainian').translate(text=text)
                    message = f"🔹 Original: {text}\n\nПереклад: {translated}\n\n{link['href']}"
                    print("-" * 80)
                    
                    if minutes < 30:  # Check if news posted 
                        fresh_news.append(message)
            except ValueError:
                break

        if fresh_news:
            for news_item in fresh_news:
                await bot.send_message(chat_id=CHAT_ID, text=news_item)
        else:
            print("No fresh news at the moment.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

