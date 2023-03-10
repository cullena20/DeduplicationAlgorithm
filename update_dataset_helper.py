# generate duplicates and add to dataframe
# write functions to generate different kinds of duplicates

from PostClass import Post

def modify_post(post: Post, content: str):
    '''
    Changes content of a post to user specified content. 
    Keeps all other information the same.
    Returns as new post (does not modify original)
    '''
    mod_post = Post()
    mod_post.manual_add(post.name, content, post.author, post.uri)
    return mod_post

def add_data(df, idx, post, duplicate=True):
    '''
    Takes entry given by idx and adds a copy of it to the dataframe.
    Changes the second post in the duplicated row to the post supplied.
    '''
    df.loc[len(df.index)] = [df.iloc[idx]["name1"], df.iloc[idx]["content1"], df.iloc[idx]["author1"], df.iloc[idx]["uri1"], df.iloc[idx]["Object1"], post.name, post.content, post.author, post.uri, post, duplicate]