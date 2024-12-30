import spacy
from textblob import TextBlob
from deep_translator import GoogleTranslator
import csv
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt



def Parser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_=['newsline'])

    quote = quotes[0]



    time_pattern = re.compile(r'^\d{2}:\d{2}$')

    data = quote.text.split('\n')
    data = [item for item in data if item != '' and not time_pattern.match(item)]
    print(data)
    print('------------------------------------------------------------------------------')

    return data


url = 'https://www.rbc.ua/rus/news/'
data = Parser(url)


nlp = spacy.load("uk_core_news_sm")

def classify_sentiment(text):
    translated_text = GoogleTranslator(source='uk', target='en').translate(text)

    blob = TextBlob(translated_text)

    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        sentiment_label = "positive"
    elif polarity < -0.3:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"
    return sentiment_label

if __name__ == '__main__':

    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

    with open("result.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Text", "Sentiment"])  # Запис заголовків


        for text in data:

            sentiment = classify_sentiment(text)
            writer.writerow([text, sentiment])
            sentiment_counts[sentiment] += 1

    print("Аналіз завершено. Результати:")
    print(f"Кількість новин: {len(data)}")
    print(f"Позитивних: {sentiment_counts['positive']}")
    print(f"Нейтральних: {sentiment_counts['neutral']}")
    print(f"Негативних: {sentiment_counts['negative']}")
    labels = ['Позитивні', 'Нейтральні', 'Негативні']
    sizes = [sentiment_counts['positive'], sentiment_counts['neutral'], sentiment_counts['negative']]


    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Аналіз')
    plt.axis('equal')
    plt.show()
