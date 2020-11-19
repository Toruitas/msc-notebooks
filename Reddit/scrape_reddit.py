#!/usr/bin/env python
import os
import re
import praw
import pprint
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# for sub in subs:
#   res = requests.get(sub.url)
#   if (res.status_code == 200 and 'content-type' in res.headers and
#       res.headers.get('content-type').startswith('text/html')):
#     html = res.text

def get_reddit():
    return praw.Reddit(
        client_id = os.environ.get('CLIENT_ID'),
        client_secret = os.environ.get('CLIENT_SECRET'),
        grant_type = 'client_credentials',
        user_agent='PRAW-Toru1', 
        username=os.environ.get('USERNAME'), 
        password=os.environ.get('PASSWORD')
    )


def get_top(subreddit_name):
    today = datetime.now().strftime(r'%Y-%m-%d')
    dirname = os.path.join('news-%s' % today, subreddit_name)
    os.makedirs(dirname, exist_ok=True)

    # Get top 50 submissions from reddit
    reddit = get_reddit()
    top_subs = reddit.subreddit(subreddit_name).top(limit=50)

    # Remove those submissions that belongs to reddit
    subs = [sub for sub in top_subs if not sub.domain.startswith('self.')]

    count = 10
    while subs and count > 0:
        sub = subs.pop(0)
        article = get_article(sub.url)
        if article:
            text = '\n\n'.join(article['content'])
            filename = re.sub(r'\W+', '_', article['title']) + '.md'
            open(os.path.join(dirname, filename), 'w').write(text)
            count -= 1


def get_article(url):
    print('  - Retrieving %s' % url)
    try:
        res = requests.get(url)
        if (res.status_code == 200 and 'content-type' in res.headers and
                res.headers.get('content-type').startswith('text/html')):
            article = parse_article(res.text)
            print('      => done, title = "%s"' % article['title'])
            return article
        else:
            print('      x fail or not html')
    except Exception:
        pass


def parse_article(text):
    soup = BeautifulSoup(text, 'html.parser')

    # find the article title
    h1 = soup.body.find('h1')

    # find the common parent for <h1> and all <p>s.
    root = h1
    while root.name != 'body' and len(root.find_all('p')) < 5:
        root = root.parent

    if len(root.find_all('p')) < 5:
        return None

    # find all the content elements.
    ps = root.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre'])
    ps.insert(0, h1)
    content = [tag2md(p) for p in ps]

    return {'title': h1.text, 'content': content}


def tag2md(tag):
    if tag.name == 'p':
        return tag.text
    elif tag.name == 'h1':
        return f'{tag.text}\n{"=" * len(tag.text)}'
    elif tag.name == 'h2':
        return f'{tag.text}\n{"-" * len(tag.text)}'
    elif tag.name in ['h3', 'h4', 'h5', 'h6']:
        return f'{"#" * int(tag.name[1:])} {tag.text}'
    elif tag.name == 'pre':
        return f'```\n{tag.text}\n```'


def main():
    subreddits = ['politics', 'worldnews', 'news']
    for sr in subreddits:
        print('Scraping /r/%s...' % sr)
        get_top(sr)


if __name__ == '__main__':
    main()