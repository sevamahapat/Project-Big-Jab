# file : youtube.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : Fetch top 10 pro vaccination videos and store its transcription for keyword extraction

# imported by: keywords.py

import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from selenium import webdriver
import time

def fetch_yt_links():
    links = []
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com")

    time.sleep(2)
    search = driver.find_element(by='xpath', value='/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div['
                                                   '2]/ytd-searchbox/form/div[1]/div[1]/input')
    search.send_keys("pro vaccination")
    search_btn = driver.find_element(by='xpath', value='/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div['
                                                       '2]/ytd-searchbox/button/yt-icon')
    search_btn.click()
    time.sleep(3)

    filter_btn = driver.find_element(by='xpath', value='//*[@id="container"]/ytd-toggle-button-renderer/yt-button'
                                                       '-shape/button/yt-touch-feedback-shape/div/div[2]')

    filter_btn.click()
    time.sleep(5)

    video_filter = driver.find_element(by='xpath', value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div['
                                                         '1]/ytd-two-column-search-results-renderer/div['
                                                         '2]/div/ytd-section-list-renderer/div[1]/div['
                                                         '2]/ytd-search-sub-menu-renderer/div['
                                                         '1]/iron-collapse/div/ytd-search-filter-group-renderer['
                                                         '2]/ytd-search-filter-renderer[1]/a/div/yt-formatted-string')

    video_filter.click()

    time.sleep(4)

    filter_btn = driver.find_element(by='xpath', value='//*[@id="container"]/ytd-toggle-button-renderer/yt-button'
                                                       '-shape/button/yt-touch-feedback-shape/div/div[2]')
    filter_btn.click()
    time.sleep(5)

    caption_filter = driver.find_element(by='xpath', value='/html/body/ytd-app/div['
                                                           '1]/ytd-page-manager/ytd-search/div['
                                                           '1]/ytd-two-column-search-results-renderer/div['
                                                           '2]/div/ytd-section-list-renderer/div[1]/div['
                                                           '2]/ytd-search-sub-menu-renderer/div['
                                                           '1]/iron-collapse/div/ytd-search-filter-group-renderer['
                                                           '4]/ytd-search-filter-renderer['
                                                           '4]/a/div/yt-formatted-string')

    caption_filter.click()

    time.sleep(5)

    user_data = driver.find_elements(by='xpath', value='//*[@id="video-title"]')

    for i in user_data:
        link = i.get_attribute('href')
        if link is None:
            continue
        elif 'watch?v=' in link:
            links.append(link)
        if len(links) == 10:
            break

    print(len(links))

    f = open('yt_links.txt', 'w')
    for i in links:
        f.write(i + '\n')

    f.close()


def transcribe_yt_links():
    srts = []
    with open('yt_links.txt') as f:
        for i in f:
            try:
                srt = YouTubeTranscriptApi.get_transcript(i[32:], languages=['en', 'en-US'])
                srts.append(srt)
            except:
                print('CANNOT TRANSCRIBE')

    return srts


def store_data_in_df(srts):
    cols = {
        'text': [],
        'start': [],
        'duration': []
    }
    df = pd.DataFrame(cols)

    for video in srts:
        for line in video:
            df = pd.concat([df, pd.DataFrame(line, index=[0])], ignore_index=True)
    return df

def scrape_youtube():
    subtitles = transcribe_yt_links()
    df = store_data_in_df(subtitles)
    file = open('covid_data.txt', 'a', encoding='utf8')
    for line in df['text']:
        file.write(line.strip())
    file.close()
    print("Youtube data scraped")
