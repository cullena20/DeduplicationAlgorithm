# use this file to add new posts after the initial file
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PostClass import Post
import pull_posts
import pickle
import config

posts: list[Post] = list()
reddit = pull_posts.log_in_reddit(config.r_client_id, config.r_client_secret, config.r_user_agent)
posts = pull_posts.n_pull_reddit(reddit, posts)
df = pull_posts.posts_to_dataframe(posts)

with open('/Users/cullen/Desktop/Gobo/Datasets/posts2.pickle', 'wb') as file:
    pickle.dump(df, file)

df.to_csv('/Users/cullen/Desktop/Gobo/Datasets/posts2.csv')