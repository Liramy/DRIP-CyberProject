import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE

import xgboost as xgb
from tqdm import tqdm
import keras
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import GridSearchCV,train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline,linear_model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from keras.preprocessing import sequence
from keras import layers, models, optimizers
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import seaborn as sn
from gensim.models.keyedvectors import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from nltk import word_tokenize

train_articles = os.listdir("datasets/train-articles")
train_labels_tags_span = os.listdir("datasets/train-labels-task1-span-identification")
train_tags_technique = os.listdir("datasets/train-labels-task2-technique-classification")
train_articles.sort()
train_labels_tags_span.sort()

# Dictionary containing news articlc
propTagsSpan = {}

for i in range(len(train_articles)):
    article = train_articles[i]
    # removing .txt file extension
    articleNoExt = os.path.splitext(article)[0]
    # replace train articles with the same name
    train_articles[i] = articleNoExt
    # removing article
    articleNo = articleNoExt.replace('article', '')
    tagPath = "datasets/train-labels-task1-span-identification/" + articleNoExt + ".task1-SI.labels"
    with open(tagPath) as r:
        tags = r.readlines()
        for i in range(len(tags)):
            tag = tags[i]
            tag = tag.replace("\t", " ")
            tag = tag.replace("\n", " ")
            tags[i] = tag
        propTagsSpan[articleNoExt] = tags
    r.close()

print(propTagsSpan[train_articles[0]])

propagandaTagTechnique = os.listdir("datasets/train-labels-task2-technique-classification")
propagandaTagTechnique.sort()
propTagsTechnique = {}

for i in range(len(train_articles)):
    article = train_articles[i]
    # removing .txt file extension
    articleNoExt = os.path.splitext(article)[0]
    # replace train articles with the same name
    train_articles[i] = articleNoExt
    # removing article
    articleNo = articleNoExt.replace('article', '')
    tagPath = "datasets/train-labels-task2-technique-classification/" + articleNoExt + ".task2-TC.labels"

    with open(tagPath) as r:
        tags = r.readlines()
        for i in range(len(tags)):
            tag = tags[i]
            tag = tag.replace(articleNo, " ")
            tag = tag.replace("\t", " ")
            tag = tag.replace("\n", " ")
            tags[i] = tag
        propTagsTechnique[articleNoExt] = tags
    r.close()

print(propTagsTechnique[train_articles[0]])

propoganda_sent_span = []

for article in train_articles:
    article_path = "datasets/train-articles/" + article + ".txt"
    tags = propTagsSpan[article]

    with open(article_path, encoding="utf-8") as r:
        entireArticle = r.read()
        for tag in tags:
            tag = tag.split()
            start = int(tag[1])
            end = int(tag[2])

            tag_line = entireArticle[start:end]
            tag_line = tag_line.replace("\n", " ")
            tag_line = tag_line.replace("\t", " ")

            propoganda_sent_span.append(tag_line)
    r.close()

print(propoganda_sent_span[0])

propoganda_techniques = {}
propoganda_techniques["Sentence"] = []
propoganda_techniques["Technique"] = []

for article in train_articles:
    article_path = "datasets/train-articles/" + article + ".txt"
    tags = propTagsTechnique[article]

    with open(article_path, encoding="utf-8") as r:
        entireArticle = r.read()
        for tag in tags:
            tag = tag.split()
            propoganda_techniques["Technique"].append(tag[0])
            start = int(tag[1])
            end = int(tag[2])

            tag_line = entireArticle[start:end]
            tag_line = tag_line.replace("\n", " ")
            tag_line = tag_line.replace("\t", " ")
            propoganda_techniques["Sentence"].append(tag_line)
    r.close()

df = pd.DataFrame.from_dict(propoganda_techniques)
propoganda_techniques_tags = ['Appeal_to_Authority','Name_Calling,Labeling','Slogans', 'Loaded_Language','Appeal_to_fear-prejudice','Repetition','Doubt','Exaggeration,Minimisation','Flag-Waving','Causal_Oversimplification','Whataboutism,Straw_Men,Red_Herring','Black-and-White_Fallacy','Thought-terminating_Cliches','Bandwagon,Reductio_ad_hitlerum']
plt.figure(figsize=(10,4))
df.Technique.value_counts().plot(kind='bar');

df = df[np.logical_not(df['Technique'].isin(['Appeal_to_Authority','Slogans','Appeal_to_fear-prejudice','Flag-Waving','Causal_Oversimplification','Whataboutism,Straw_Men,Red_Herring','Black-and-White_Fallacy','Thought-terminating_Cliches','Bandwagon,Reductio_ad_hitlerum']))]
plt.figure(figsize=(10,4))
df.Technique.value_counts().plot(kind='bar');

nltk.download("stopwords")

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
# BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def clean_text(text):
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    # text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if
                    word not in STOPWORDS)  # delete stopwors from text - not sure if we want to do this
    return text


df['Sentence'] = df['Sentence'].apply(clean_text)

df['Sentence'].apply(lambda x: len(x.split(' '))).sum()

X = df.Sentence
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)
X.shape

le = preprocessing.LabelEncoder()
le.fit(df['Technique'])
y = le.transform(df['Technique'])
y.shape

set(le.inverse_transform(y))

#random_state sets a seed, the train-test splits are always deterministic. If the seed is not set, train-test splits are different each time
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)

smote = SMOTE(sampling_strategy='not majority')

x_smote, y_smote = smote.fit_resample(X_train, y_train)
x_smote.shape, y_smote.shape

from sklearn.metrics import precision_score
nb =  MultinomialNB()
nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)

## Evaluating the model
print("Accuracy: ", accuracy_score(y_test, y_pred)* 100)
precision, recall, F1, support = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division = 1)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 score: ", F1)

y_test_plot = list(le.inverse_transform(y_test))
y_pred_plot = list(le.inverse_transform(y_pred))
data = confusion_matrix(y_test_plot, y_pred_plot)
df_cm = pd.DataFrame(data, columns=np.unique(y_test_plot), index = np.unique(y_test_plot))
df_cm.index.name = 'Actual'
df_cm.columns.name = 'Predicted'
plt.figure(figsize = (10,7))
sn.set(font_scale=1.4)
sn.heatmap(df_cm, cmap="Blues", annot=True,annot_kws={"size": 16})# font siz

glove2word2vec(glove_input_file="glove.6B/glove.6B.100d.txt", word2vec_output_file="gensim_glove_vectors.txt")
model_news = KeyedVectors.load_word2vec_format('gensim_glove_vectors.txt', binary=False)
model_news.save_word2vec_format('glove.6B.100d.bin', binary=True)

nltk.download('punkt')
review_embeddings = []
for each_review in df.Sentence:
    Review_average = np.zeros(model_news.vector_size)
    count_val = 1

    for each_word in word_tokenize(each_review):
        if (each_word.lower() in model_news):
            Review_average = + model_news[each_word.lower()]
            count_val += 1

    review_embeddings.append(list(Review_average / count_val))

embedding_data = pd.DataFrame(review_embeddings)
embedding_data = embedding_data.fillna(0)
print(embedding_data.shape)

le = preprocessing.LabelEncoder()
le.fit(df['Technique'])
y = le.transform(df['Technique'])
print(y.shape)
X_train_embed_news, X_test_embed_news, y_train_embed_news, y_test_embed_news =  \
                            train_test_split(embedding_data,y,test_size = 0.2,random_state = 0)

sgd = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)
sgd.fit(X_train_embed_news, y_train_embed_news)

y_pred = sgd.predict(X_test_embed_news)

## Evaluating the model
print("Accuracy: ", accuracy_score(y_test_embed_news, y_pred)* 100)
precision, recall, F1, support = precision_recall_fscore_support(y_test_embed_news, y_pred, average='macro', zero_division = 1)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 score: ", F1)