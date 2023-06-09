# file : reddit.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : Fetch top reddit posts from subreddits like r/DebateVaccines, r/CovidVaccinated, r/vaxxhappened, r/Vaccine
#           from reddit api

# imported by: keywords.py

import praw
from twitter import remove_emojis

user_agent = "praw_scraper_1.0"

reddit = praw.Reddit(username="dhwanisanmukhani",
                     password="N2BfR#@Xx!xQ8yj",
                     client_id="lPukaWWirZWacAQH3ykHuQ",
                     client_secret="9x5ta12rGY_oWvcbK0xANoi93N262g",
                     user_agent=user_agent
                     )

def get_posts(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    reddit_file = open('covid_data.txt', 'a', encoding='utf8')

    for submission in subreddit.top(limit=40):
        text = remove_emojis(submission.title)
        reddit_file.write(text +"\n")

    reddit_file.close()


def scrape_reddit():
    subreddits = ["DebateVaccines", "CovidVaccinated", "vaxxhappened", "Vaccine"]
    for topic in subreddits:
        get_posts(topic)
    print("Reddit data scraped")

