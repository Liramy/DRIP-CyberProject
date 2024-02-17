import joblib
import GoogleNews
from newspaper import Article
import base64

class ArticleFinder():
    """Define an object of type <ArticleFinder> for getting articles off the internet

    :param configs: Contains the list of configs for the search results
    :type configs: dict

    :returns: An object for getting articles of the internet
    :rtype: ArticleFinder
    """

    def __init__(self, configs):
        self.subject = configs['subject']
        self.language = configs['lang']
        self.period = configs['period']

        self.google_search = GoogleNews.GoogleNews(lang=self.language)
        self.google_search.enableException(True)
        self.google_search.setperiod(self.period)
        self.google_search.set_encode('utf-8')
        self.google_search.get_news(self.subject)

        max_articles_number = 25
        self.articleLinkList = self.google_search.get_links()[:max_articles_number]

    def close(self):
        self.google_search.clear()


dicty = {"subject": "racism", "lang": "en", "period": "4y"}
finderz = ArticleFinder(dicty)

print(finderz.articleLinkList)

google_url = "https://news.google.com/articles/CBMiZmh0dHBzOi8vd3d3LnB1c2hzcXVhcmUuY29tL2d1aWRlcy9ob3Jpem9uLWZvcmJpZGRlbi13ZXN0LWJ1cm5pbmctc2hvcmVzLWFsbC1kZWx2ZXJzLXRyaW5rZXRzLWxvY2F0aW9uc9IBAA?hl=en-CA&gl=CA&ceid=CA%3Aen"
base64_url = google_url.replace("https://news.google.com/articles/","").split("?")[0]
actual_url = base64.b64decode(base64_url)[4:-3].decode('utf-8')
print(actual_url)