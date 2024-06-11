from openai import OpenAI
import os
import time
import sys

# Load ENV file
from dotenv import load_dotenv
load_dotenv()
krutrim_api = os.getenv('krutrim_api')


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Scrape_news')))
from news import getNews


def ConvertedNews():
  news= getNews("business")

  articles = []
  for item in news['data']:
    articles.append({
      'title': item['title'],
      'content': item['content'],
      'date': item['date'],
      'time': item['time']
    })

  openai = OpenAI(
      api_key=krutrim_api,
      base_url="https://cloud.olakrutrim.com/v1",
  )



  converted_news=[]
  for item in articles:
    

    chat_completion = openai.chat.completions.create(
      model="Krutrim-spectre-v2",

      messages=[
        {"role": "system", "content": """translate the below news into Hinglish(English + hindi)  spoken by an indian male in his 30s make it formal as it is an news. remember to add punctuations"""},
        {"role": "user", "content": item['content']}],
      )
    Hindi=chat_completion.choices[0].message.content
    time.sleep(10)
    converted_news.append({
      'title': item['title'],
      'content': item['content'],
      'Hindi': Hindi
    })

    return converted_news
