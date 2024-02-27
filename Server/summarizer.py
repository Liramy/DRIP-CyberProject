import os
from openai import OpenAI
from ArticleScrapping import ArticleScrapper

scrapper = ArticleScrapper("Avatar the Last Airbender", '2y', 'En')
completed_articles = []
for article in scrapper.article_array:
    complete_text = '.'.join(article)

client = OpenAI(api_key="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")

combined_content = client.completions.create(
    model="davinci-002",
    prompt="Here are articles, please combine them into one article: \n".join(completed_articles[:4]),
    max_tokens=1500  # Adjust max_tokens based on desired length
)

print(combined_content['choices'][0]['text'])
