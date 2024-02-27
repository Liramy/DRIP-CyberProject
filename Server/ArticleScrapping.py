import joblib
import sklearn
import GoogleNews
from newspaper import Article
import base64
from urllib.parse import urlparse, parse_qs, unquote


class ArticleFinder():
    """Define an object of type <ArticleFinder> for getting articles off the internet

    :param configs: Contains the list of configs for the search results
    :type configs: dict

    :returns: An object for getting articles of the internet
    :rtype: ArticleFinder
    """

    def __init__(self, subject, language, period):
        self.subject = subject
        self.language = language
        self.period = period

        self.model = joblib.load("PropDetectionModel.mdl")
        self.count_vectorize = joblib.load("CountVectorizer.vct")

        self.google_search = GoogleNews.GoogleNews(lang=self.language)
        self.google_search.enableException(True)
        self.google_search.setperiod(self.period)
        self.google_search.set_encode('utf-8')
        self.google_search.get_news(self.subject)

        max_articles_number = 25
        self.articleLinkList = self.google_search.get_links()[:max_articles_number]
        for i in range(len(self.articleLinkList)):
            self.articleLinkList[i] = self.decipher_url(self.articleLinkList[i])

        self.create_propaganda_isolation()

    def close(self):
        self.google_search.clear()

    def decipher_url(self, encrypted_url):
        parsed_url = urlparse(encrypted_url)
        encoded_path = parsed_url.path.split("/")[-1]
        decoded_path = unquote(encoded_path)

        query_params = parse_qs(parsed_url.query)

        if 'hl' in query_params:
            language = query_params['hl'][0]
        else:
            language = 'en'  # Default to English if 'hl' parameter is not present

        return f'https://news.google.com/articles/{decoded_path}?hl={language}'

    def create_propaganda_isolation(self):
        article_array = []
        for article_url in self.articleLinkList:
            try:
                article = Article(article_url)
                article.download()
                article.parse()
                exclude_chars = ["", ".", "\n"]

                # Split the text into an array of words, excluding specified characters
                text = [sentence.strip() for sentence in article.text.split('.') if
                        sentence.strip() not in exclude_chars]
                article_array.append(text)
            except Exception as e:
                pass
        i = 0
        self.predsArticles = []
        for article_text in article_array:
            if len(article_text) < 3:
                pass
            x_value = self.count_vectorize.transform(article_text)
            predictions = self.model.predict(x_value)
            count_of_ones = sum(1 for value in predictions if value == 1)
            average_prediction = (count_of_ones / len(predictions))
            self.predsArticles.append((article_text, average_prediction))

    def return_preds(self):
        return self.predsArticles
