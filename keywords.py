# file : keywords.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : Reads the data from twitter, reddit and youtube. Does a sentiment check ie if the text is in a positive tone
#           and then uses yake to extract keywords to form a wordcloud

# imports : twitter.py, reddit.py, youtube.py
# imported by: covid_main.pyw

import string
import yake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.stem import WordNetLemmatizer

from twitter import scrape_twitter
from reddit import scrape_reddit
from youtube import scrape_youtube

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')


def polarity(data):
    sent_analyse = SentimentIntensityAnalyzer()
    data = [line for line in data if sent_analyse.polarity_scores(line)['compound'] > 0]
    return data


def keyword_extractor(data):
    text = " ".join(data)
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 300
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    keywords_list = []
    for kw in keywords:
        keywords_list.append(kw[0])
    return keywords_list


def create_word_cloud(data):
    data = data
    for i in range(len(data)):
        data[i] = str.lower(data[i])
    wc = WordCloud(max_words=300, width=1200, height=1000,
                   collocations=False).generate(" ".join(data))
    plt.figure(figsize=(20, 8))
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


def handle_punctuations(data):
    translator = str.maketrans('', '', string.punctuation)
    return data.translate(translator)


def lemmatize(data):
    lemmatizer = WordNetLemmatizer()
    cleaned_data = []
    for line in data:
        line_tokens = nltk.word_tokenize(line)
        stemmed_words = [lemmatizer.lemmatize(word) for word in line_tokens]
        text = handle_punctuations(" ".join(stemmed_words))
        cleaned_data.append(text)
    return cleaned_data


def getKeywords():
    data = [line.strip() for line in open('covid_data.txt', encoding='utf8')]
    positive_data = polarity(data)
    cleaned_data = lemmatize(positive_data)
    keywords = keyword_extractor(cleaned_data)
    return cleaned_data, keywords


def make_word_cloud(text):
    create_word_cloud(text)


def getData():
    scrape_twitter()
    scrape_reddit()
    scrape_youtube()
    print('Making a WordCloud...')
    cleaned_data, keywords = getKeywords()
    make_word_cloud(keywords)


if __name__ == '__main__':
    getData()
