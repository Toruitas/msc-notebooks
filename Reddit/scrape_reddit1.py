#! /usr/bin/env python

import os
import re
import praw
import pprint
import requests
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

reddit = praw.Reddit(
        client_id = "2iwsUgs_HlruwQ",
        client_secret = "FIY-isQc8xsVbaQ0PO9exMv4XXw",
        grant_type='password',
        user_agent='PRAW-Toru1', 
        username=os.environ.get('USERNAME'), 
        password=os.environ.get('PASSWORD')
    )


def get_date(created):
    return datetime.fromtimestamp(created)

subreddit = reddit.subreddit('news')

time_filters = ["all", "day", "hour", "month", "week", "year"]
for timeframe in time_filters:

    # controversial_topics_dict = { 
    #     "title":[], 
    #     "score":[],
    #     "upvote_ratio":[],
    #     "id":[], 
    #     "url":[], 
    #     "comms_num": [], 
    #     "created": [], 
    #     "body":[]
    # }

    # controversial_subreddit = subreddit.controversial(time_filter=timeframe,limit=1000)  # .hot, .new, .controversial, .top, and .gilded

    # for submission in controversial_subreddit:
    #     controversial_topics_dict["title"].append(submission.title)
    #     controversial_topics_dict["score"].append(submission.score)
    #     controversial_topics_dict["upvote_ratio"].append(submission.upvote_ratio)
    #     controversial_topics_dict["id"].append(submission.id)
    #     controversial_topics_dict["url"].append(submission.url)
    #     controversial_topics_dict["comms_num"].append(submission.num_comments)
    #     controversial_topics_dict["created"].append(submission.created)
    #     controversial_topics_dict["body"].append(submission.selftext)
    
    # controversial_topics_data = pd.DataFrame(controversial_topics_dict)

    # _timestamp = controversial_topics_data["created"].apply(get_date)
    # controversial_topics_data = controversial_topics_data.assign(timestamp = _timestamp)

    # controversial_topics_data.to_csv(f'controversial-{timeframe}.csv', index=False)

    # print(f'controversial-{timeframe}.csv saved')

    # sleep(1)

    top_topics_dict = {
        "title":[], 
        "score":[],
        "upvote_ratio":[],
        "id":[], 
        "url":[], 
        "comms_num": [], 
        "created": [], 
        "body":[]
    }

    top_subreddit = subreddit.top(time_filter=timeframe,limit=1000)

    for submission in top_subreddit:
        top_topics_dict["title"].append(submission.title)
        top_topics_dict["score"].append(submission.score)
        top_topics_dict["upvote_ratio"].append(submission.upvote_ratio)
        top_topics_dict["id"].append(submission.id)
        top_topics_dict["url"].append(submission.url)
        top_topics_dict["comms_num"].append(submission.num_comments)
        top_topics_dict["created"].append(submission.created)
        top_topics_dict["body"].append(submission.selftext)

    top_topics_data = pd.DataFrame(top_topics_dict)

    _timestamp = top_topics_data["created"].apply(get_date)
    top_topics_data = top_topics_data.assign(timestamp = _timestamp)

    top_topics_data.to_csv(f'top-{timeframe}.csv', index=False)

    print(f'top-{timeframe}.csv saved')

    sleep(1)


