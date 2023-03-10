class Post:
  def __init__(self, name=None, content=None, author=None, uri=None):
    self.name = name
    self.content = content
    self.author = author
    self.uri = uri

  def from_tweet(self, tweet, uname):
    self.name = None
    self.content = tweet.text
    self.author = "https://twitter.com/" + uname
    self.uri = "https://twitter.com/" + uname + "/status/" + str(tweet.id)

  def from_reddit(self, post):
    self.name = post.title
    self.content = post.selftext # maybe selftext_html
    self.author = str(post.author) # add link if we want to make this a link
    self.uri = "https://reddit.com" + post.permalink

  def from_toot(self, toot):
    self.name = None
    self.content = toot.content
    self.author = toot.account.url
    self.uri = toot.url

  # perhaps unnecessary
  def manual_add(self, name=None, content=None, author=None, uri=None):
    self.name = name
    self.content = content
    self.author = author
    self.uri = uri

  # useful for testing - note this function is not inplace
  def swap_content_name(self):
    swapped = Post(name=self.content)
    return swapped

  def __str__(self):
    return f'Name: {self.name}, Content: {self.content}, Author: {self.author}, Uri: {self.uri}'

post1 = Post(content="")

