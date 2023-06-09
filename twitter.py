# file : twitter.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : Fetch recent tweets on hashtags #getVaccinated and #VaccinesWork from twitter

# imported by: keywords.py

import pandas as pd
import tweepy
import re

def remove_emojis(data):
	emojis = re.compile("["
	u"\U00002700-\U000027BF"  # Dingbats
	u"\U0001F600-\U0001F64F"  # Emoticons
	u"\U00002600-\U000026FF"  # Miscellaneous Symbols
	u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
	u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
	u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
	u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
	u"\U0001F198"
	"]+", re.UNICODE)
	return re.sub(emojis, '', data)

# Remove extra spaces, emojis, mentions, links and hashtags from tweets
def clean_tweet(text):

	text = text.replace('\n', ' ')
	text = text.replace('\t', ' ')

	text = " ".join(
		word for word in text.split(' ') if not (word.startswith("#") or word.startswith("http") or word.startswith("@"))
	)
	text = remove_emojis(text)
	return text


def scrape_topic(api, words, date_since, numtweet):
		twitter_file = open('covid_data.txt', 'w', encoding='utf8')
		db = pd.DataFrame(columns=['description',
								'following',
								'followers',
								'totaltweets',
								'retweetcount',
								'likecount',
								'text',
								'json'])

		tweets = tweepy.Cursor(api.search_tweets,
							words, lang="en",
							since_id=date_since,
							tweet_mode='extended',
							result_type='mixed').items(numtweet)
		list_tweets = [tweet for tweet in tweets]

		for tweet in list_tweets:
				description = tweet.user.description
				following = tweet.user.friends_count
				followers = tweet.user.followers_count
				totaltweets = tweet.user.statuses_count
				retweetcount = tweet.retweet_count
				likecount = tweet.favorite_count
				json = tweet._json

				try:
						text = tweet.retweeted_status.full_text
				except AttributeError:
						text = tweet.full_text

				if text in db['text']:
					continue
				text = clean_tweet(text)
				twitter_file.write(text + "\n")
				ith_tweet = [description, following,
							 followers, totaltweets, retweetcount,
							 likecount ,text, json]
				db.loc[len(db)] = ith_tweet

		twitter_file.close()


def scrape_twitter():
		token = 'AAAAAAAAAAAAAAAAAAAAAJzpjQEAAAAAxsxh3oqNchxJXDln%2Fx%2FL4AauG4g%3DWy6C7adAP9PoQiH6KRRG2IuffNbJQs2fhbkyd4rVoLmcK9DS8w'


		auth = tweepy.OAuth2BearerHandler(token)
		api = tweepy.API(auth)

		hashtags = ['getVaccinated', 'VaccinesWork']
		date_since = '2021-01-01'

		numtweet = 100

		[scrape_topic(api, word, date_since, numtweet) for word in hashtags]
		print('Twitter data scraped')

