# pull posts from reddit, twitter, and mastodon - put into dataframe and pickle

# todo
# improve way that posts are pulled

import config
import praw
import tweepy
from mastodon import Mastodon
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PostClass import Post
import pandas as pd
import pickle

posts: list[Post] = list()

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
    Posts here are filtered such that they have only have a title and no content.
    This eliminates most posts in Reddit that only have a title and perhaps a photo or video.
    This also filters out NSFW posts.
    '''
    subreddit = reddit.subreddit('popular')
    # Because majority of popular reddit posts have no content, setting limit to 500 pulls around 30 posts
    for submission in subreddit.hot(limit=500):
        if submission.over_18 == False and submission.selftext_html != None:
            sub = Post()
            sub.from_reddit(submission)
            posts.append(sub)
    return posts

def n_pull_reddit(reddit, posts, limit=50):
    '''
    Pulls reddit posts, converts them into Post class, and appends them to a provided list.
    Reddit posts are pulled from the popular subreddit and are sorted by hot
    '''
    subreddit = reddit.subreddit('popular')
    # change how this is done
    for submission in subreddit.hot(limit=limit):
        if submission.over_18 == False:
            sub = Post()
            sub.from_reddit(submission)
            posts.append(sub)
    return posts

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

def posts_to_dataframe(posts):
    '''
    Stores a list of post objects as a dataframe
    '''
    df = pd.DataFrame([[p.name, p.content, p.author, p.uri, p] for p in posts], columns = ["name1", "content1", "author1", "uri1", "Object1"])
    return df

if __name__ == "__main__":
    reddit = log_in_reddit(config.r_client_id, config.r_client_secret, config.r_user_agent)
    posts = pull_reddit(reddit, posts)

    twitter = log_in_twitter(config.t_bearer_token, config.t_consumer_key, config.t_consumer_secret, config.t_access_token, config.t_access_token_secret)
    posts = pull_twitter(twitter, posts)

    mastodon = log_in_mastodon(config.m_client_id, config.m_client_secret, config.m_access_token, config.m_api_base_url)
    posts = pull_mastodon(mastodon, posts)

    df = posts_to_dataframe(posts)

    # This was originally run to generate posts.pickle and posts.csv, which I manually placed in the Datasets folder
    # I am not refactoring this so that if this file is run, it will generate new posts files not to be placed in this folder,
    # that won't overide the original files
    with open('posts.pickle', 'wb') as file:
        pickle.dump(df, file)

    # 'Unnamed' index column is added in this step, put index = False if we don't want this 
    # This is a dataset of posts pulled, not a dataset that can be used to test the code (this requires pairs of posts and labels)
    df.to_csv('posts.csv')

    # functions that allow you to pull posts with more specifity would be useful
