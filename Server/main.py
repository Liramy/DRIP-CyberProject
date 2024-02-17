import joblib
import GoogleNews


# searcher = GoogleNews.GoogleNews(lang='en')
# searcher.enableException(True)
# searcher.setperiod(period='2y')
# searcher.get_news('Spongebob')
# a = searcher.result(sort=True)

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
        self.google_search.get_news(self.subject)

        max_articles_number = 25
        self.articleLinkList = self.google_search.get_links()[:max_articles_number]

    def close(self):
        self.google_search.clear()


dicty = {"subject": "racism", "lang": "en", "period": "4y"}
finderz = ArticleFinder(dicty)

print(len(finderz.articleLinkList))
