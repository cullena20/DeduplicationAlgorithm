# pull posts from reddit, twitter, and mastodon - put into dataframe and pickle

# todo
# improve way that posts are pulled

import praw
import tweepy
from mastodon import Mastodon
from PostClass import Post
import pandas as pd
import pickle

r_client_id = "etCTL0OgGAY1jA"
r_client_secret = "vMtYIGE5WVK8BDczKh7ZnRup3rb3ew"
r_user_agent = "Conscious-Reply-7037"

posts = list()

def log_in_reddit(client_id, client_secret, user_agent):
    '''
    Returns a Reddit instance given a user's credentials.
    '''
    reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent)
    return reddit


def pull_reddit(reddit, posts):
    '''
    Pulls reddit posts, converts them into Post class, and appends them to a provided list.
    Reddit posts are pulled from the popular subreddit and are sorted by hot
    '''
    subreddit = reddit.subreddit('popular')
    # change how this is done
    for submission in subreddit.hot(limit=500):
        if submission.over_18 == False and submission.selftext_html != None:
            sub = Post()
            sub.from_reddit(submission)
            posts.append(sub)
    return posts

t_bearer_token = "AAAAAAAAAAAAAAAAAAAAAHT7lAEAAAAAJCMSxuSwOOZlPpRoSMapdTTQAM8%3DWzjOlhZ3aybgCB5GLU0yK6A6PZI8uuSmlLrFq2WeJ7PhRiG94q"
t_consumer_key = "tK6DEzcOQWjIRxdx3xPObjC6H"
t_consumer_secret = "4yrRJYNpoVhLRkAWxheIqlHfRUs5HriRXZBnKyIfhWcWPfNnrW"
t_access_token = "2696726232-3pLzWACE7F7fI7ble9n6VvXcyPMsjkeW1O4uc96"
t_access_token_secret = "mN1HmnLj7YIhV1vXrrZ05u9kf1BfnM9wu37Dsm7yi2Z1V"

def log_in_twitter(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret):
    '''
    Returns a twitter Client instance given a user's credentials.
    '''
    twitter = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
    return twitter

def pull_twitter(twitter, posts):
    '''
    Pulls twitter posts, converts them into Post class, and appends them to a provided list.
    The top 30 posts in the user's home timeline are pulled.
    '''
    tweets = twitter.get_home_timeline(max_results=30, tweet_fields=['author_id'])
    for i in tweets.data:
        # had to do this for uname cause nonsense
        uname = twitter.get_user(id=i.author_id).data.username
        sub = Post()
        sub.from_tweet(i, uname)
        posts.append(sub)
    return posts
    
m_client_id = 'SOm698kzerQmtD-q_8GPGIUa324CZY6XUUuOfClUMD4'
m_client_secret = "U3jC-ZkU4n98HpofRvvGSmhEUWskmZ-c69PvRJn381s"
m_access_token = 'Bq-ntqA-0JV24X7kqu6NnScPNXPm7QT9pVC8mMBemQ0'
m_api_base_url = "https://mastodonbooks.net"

# run the below once to initialize an app
# Mastodon.create_app(
#     client_name = 'playground',
#     api_base_url = api_base_url,
#     to_file = client_secret 
# )

def log_in_mastodon(client_id, client_secret, access_token, api_base_url):
    '''
    Returns a Mastodon instance given a user's credentials.
    '''
    mastodon = Mastodon(client_id = client_id, client_secret = client_secret, access_token = access_token, api_base_url = api_base_url)  
    return mastodon 

def pull_mastodon(mastodon, posts):
    '''
    Pulls mastodon posts, converts them into Post class, and appends them to a provided list.
    The top 30 posts in the user's home timeline are pulled.
    '''
    for post in mastodon.timeline(limit=30):
        sub = Post()
        sub.from_toot(post)
        posts.append(sub)
    return posts

reddit = log_in_reddit(r_client_id, r_client_secret, r_user_agent)
posts = pull_reddit(reddit, posts)

twitter = log_in_twitter(t_bearer_token, t_consumer_key, t_consumer_secret, t_access_token, t_access_token_secret)
posts = pull_twitter(twitter, posts)

mastodon = log_in_mastodon(m_client_id, m_client_secret, m_access_token, m_api_base_url)
posts = pull_mastodon(mastodon, posts)

df = pd.DataFrame([[p.name, p.content, p.author, p.uri, p] for p in posts], columns = ["name1", "content1", "author1", "uri1", "Object1"])

with open('posts.pickle', 'wb') as file:
    pickle.dump(df, file)

# 'Unnamed' index column is added in this step, put index = False if we don't want this 
# This is a dataset of posts pulled, not
df.to_csv('posts.csv')

# functions that allow you to pull posts with more specifity would be useful
