import joblib
import sklearn
import GoogleNews
from newspaper import Article
import base64
from urllib.parse import urlparse, parse_qs, unquote


class ArticleScrapper:
    """Define an object of type <ArticleFinder> for getting articles off the internet

    :param subject: Subject of the searching function - String
    :param period: The period of time for the search (i.e. 7d, 2m, 5y) - String
    :param max_results: max number of results for search - int
    :param language: Language with the abbreviation (En, Es ...) - String

    :returns: An object for getting articles of the internet
    :rtype: ArticleScrapper
    """

    def __init__(self, subject, period, max_results=25, language='En'):
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

        max_results = len(self.google_search.get_links()) if (
                len(self.google_search.get_links()) < max_results) else max_results
        self.articleLinkList = self.google_search.get_links()[:max_results]
        for i in range(len(self.articleLinkList)):
            self.articleLinkList[i] = self.decipher_url(self.articleLinkList[i])

        self.create_propaganda_isolation()

    def close(self):
        """Close the scrapper to not waste cpu usage"""
        self.google_search.clear()

    def decipher_url(self, encrypted_url):
        """The url given is a Google News link, those links are inherently encrypted.
           The encryption used by Google is a basic base64 cypher which is easy to decode.
           We simply decypher the path, then the language and we get the finished link.
        """
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
        """Make an array of every article and the propaganda precentege within it"""
        article_array = []
        article_dict = {}
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
                article_dict[text[0]] = article_url
            except Exception as e:
                pass
        self.refactored_dict = {}
        for article_text in article_array:
            text = article_text
            if len(article_text) < 3:
                pass
            try:
                x_value = self.count_vectorize.transform(article_text)
                predictions = self.model.predict(x_value)
                count_of_ones = sum(1 for value in predictions if value == 1)
                average_prediction = (count_of_ones / len(predictions))
                print(average_prediction)
                url = article_dict[text[0]]
                self.refactored_dict[url] = (text, average_prediction)
            except Exception as e:
                pass

    def return_dict(self):
        return self.refactored_dict