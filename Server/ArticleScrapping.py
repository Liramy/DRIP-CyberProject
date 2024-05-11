import concurrent.futures
import requests
import joblib
import GoogleNews
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
import string
import numpy as np

class ArticleScrapper:
    def __init__(self, subject, period, language='en', max_results=100):
        self.subject = subject
        self.language = language
        self.period = period
        self.max_results = max_results

        # Load model and vectorizer
        self.model = joblib.load("Server/PropDetectionModel.mdl")
        self.count_vectorizer = joblib.load("Server/CountVectorizer.vct")

        # Initialize Google News instance
        self.google_news = GoogleNews.GoogleNews(lang=self.language, region="IL")
        self.google_news.enableException(True)
        self.google_news.setperiod(self.period)
        self.google_news.search(self.subject)
        
        for i in range(1, 10):
            self.google_news.get_page(i)
        
        # Fetch article links
        self.article_links = self.google_news.get_links()[:self.max_results]

    def fetch_article(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            return None

    def process_article(self, article_text):
        if not article_text:
            return None

        # Remove punctuation and split text into sentences
        translator = str.maketrans('', '', string.punctuation)
        cleaned_text = article_text.translate(translator)
        sentences = [sentence.strip() for sentence in cleaned_text.split('.') if sentence.strip()]
        print(sentences)

        # Vectorize text
        predictions = []
        for sentence in sentences:
            x_value = self.count_vectorizer.transform(sentence)
            pred = self.model.predict(x_value)
            predictions.append(pred)

        # Calculate propaganda percentage
        sum = 0
        for pred in predictions:
            sum += pred
        average_prediction = sum / len(predictions)
        return average_prediction

    def get_results(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self.fetch_article, url): url for url in self.article_links}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    article_text = future.result()
                    propaganda_percentage = self.process_article(article_text)
                    if propaganda_percentage is not None:
                        results.append((url, propaganda_percentage))
                except Exception as e:
                    pass
        return results

    def close(self):
        self.google_news.clear()
