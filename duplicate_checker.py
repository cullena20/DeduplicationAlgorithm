from PostClass import Post
from difflib import SequenceMatcher
import re
from html2text import html2text
import urllib.request

# Post has attributes: name, content, author, uri
threshold = 0.8

def is_duplicate(post1: Post, post2: Post):
    '''
    Returns true if two posts are duplicates according to our rules, false otherwise

    General Rules
    Rule 1: Two posts have identical content
    Rule 2: Two posts have very similar text and the same media or no media (see non duplicate assumptions 1 and 2)
    Rule 3: Two posts have very similar text and are retweeting to the same tweet (PROBLEM: regex only checks retweeting same user) or not retweeting

    Two Reddit Post Rules (NEEDS MORE THOUGHT)
    Rule 4: Two Reddit posts have identical names and content (does name matter at all here, in this case it need not be explicitly coded) (no media)
    Rule 5: Two Reddit posts have very similar names and content (no media)
    ? Rule 6: Two Reddit posts have identical or very similar names (but what if content is different - perhaps sufficiently similar content)
    ? Rule 7: Two Reddit posts have identical or very similar content (this is covered in rules 1-2, does name matter at all here?)
    Rule 8: Two Reddit posts have the same author and identical or very similar content, regardless of the name.

    One Reddit Post, One Not Rules (Needs more thought, see in wild)
    Rule 9: A Reddit Post name and a non Reddit Post content are similar according to Rules 1-3 (what about content of Reddit post, also media considerations)
    Rule 10: A Reddit Post and non Reddit post have identical or very similar content. (covered in Rules 1-3) (what about name of Reddit post? media)
    
    Non Duplicate Assumptions (some intricacies may be added here)
    1 - Two posts that share different media are not duplicates, regardless of text
    2 - Two posts that are retweeting to different tweets are not duplicates, regardless of text

    Text Processing Assumptions - Content and Names are processed according to the following assumptions.
    1 - Casing does not matter. All text is converted to lower case for comparison.
    2 - Whitespace does not matter. Whitespace is removed from text.
    3 - Special characters do not matter. Special characters are removed from text (not implemented yet)
    4 - Html text may be converted to regular text by removing all tags.
    5 - Links and retweet tags do not matter. They are removed from the text and may be used in comparing media or retweet tags.
    6 - All of these above rules can be used to process any text before it is compared (maybe some exceptions should be allowed)
    '''
    # Rule 1 - if they have identical content 
    if identical_content(post1, post2):
        return True
    # Rule 2- if they have very similar content and share the same media (or do not have media) 
    # same media may have problems if images or something
    elif similar_content(post1, post2, threshold) is True and same_media(post1, post2):
        return True
    # Rule 3 - above with retweet PROBLEM THE SAME RETWEET ONLY CHECKS SAME USER SO ISN'T MEANINFFUL HERE
    elif similar_content(post1, post2, threshold) is True and same_retweet(post1, post2):
        return True
    # If both posts are Reddit Posts
    if post1.name != None and post2.name != None:
        # Rule 6 - Two Reddit Posts have identical or very similar names
        if similar_names(post1, post2, threshold): # TODO add this to duplicate dictionary
            return True
        # Rule 8 - Two Reddit Posts have similar content and the same author (regardless of name)
        elif same_author_content(post1, post2, threshold):
            return True
    # If one post is a Reddit Post and the other isn't
    # He suspects that there won't be many duplicates here
    # So checking title and tweet or tweet and body will be duplicates (we won't know til we see real world example)
    elif (post1.name == None and post2.name != None) or (post2.name == None and post1.name != None):
        # Rule 9 part 1 - if Reddit has identical name as another posts content 
        if identical_cross(post1, post2) is True:
            return True
        # Rule 9 part 2 - if Reddit has very similar name to another posts content
        elif similar_cross(post1, post2, threshold) is True:
            return True
    return False


def is_duplicate_dict(post1: Post, post2: Post):
    '''
    Given two posts, returns dictionary containing duplicate_checker results for each rule.
    This function is useful in testing the code.
    '''
    # if they have identical content
    results = dict()
    if identical_content(post1, post2):
        results["identical_content"] = True
    else: 
        results["identical_content"] = False
    # if they have very similar content and do not share the same media (or do not have media)
    if similar_content(post1, post2, threshold) is True and same_media(post1, post2):
        results["similar_content_media"] = True
    else:
        results["similar_content_media"] = False
    if similar_content(post1, post2, threshold) is True and same_retweet(post1, post2):
        results["similar_content_retweet"] = True
    else:
        results["similar_content_retweet"] = False
    # maybe this reddit part could be done better
    if post1.name != None and post2.name != None:
        if similar_names(post1, post2, threshold):
            results["similar_names"] = True
        else:
            results["similar_names"] = False
        if same_author_content(post1, post2, threshold):
            results["same_author_content"] = True
        else:
            results["same_author_content"] = False
    else:
        results["similar_names"] = False
        results["same_author_content"] = False
    # if Reddit has same title as another posts content, change this to similar text, consider intracies
    if (post1.name == None and post2.name != None) or (post2.name == None and post1.name != None):
        if identical_cross(post1, post2) is True:
            results["identical_cross"] = True
        else:
            results["identical_cross"] = False
        if similar_cross(post1, post2, threshold) is True:
            results["similar_cross"] = True
        else:
            results["similar_cross"] = False
    else:
        results["identical_cross"] = False
        results["similar_cross"] = False
    return results
    
def identical_content(post1, post2):
    '''
    Returns true if two posts have identical content, false otherwise
    The content must be truely identical, as it is not processed.
    This implements Rule 1.
    '''
    if post1.content == post2.content:
        return True
    else:
        return False

# text only rules: compare content that is all lower case, whitespace removed, links removed, html removed

# how similar content is based on some established similarity algorithm
# this algorithm cares about casing
def similar_content(post1, post2, threshold):
    '''
    Returns true if two posts have content that is similar to a certain threshold according to the SequenceMatcher algorithm, false otherwise
    This works on processed content.
    Alongside same_media, this implements Rule 2.
    Alongside same_retweet, this implements Rule 3
    '''
    content1 = process(post1.content)[0] # should i do remove unnecessary?
    content2 = process(post2.content)[0]
    similarity = SequenceMatcher(None, content1, content2).ratio()
    if similarity >= threshold:
        return True
    else:
        return False

def similar_names(post1, post2, threshold):
    '''
    Takes two Reddit posts as input and compares only their names.
    Returns true if their are similar to a certain threshold, false otherwise
    Before this is used, it should be ensured that the two posts being compared
    are Reddit posts by ensuring their titles are not equal to None.
    This implements Rule 6.
    '''
    name1 = process(post1.name)[0]
    name2 = process(post2.name)[0]
    similarity = SequenceMatcher(None, name1, name2).ratio()
    if similarity >= threshold:
        return True
    else:
        return False

def same_author_content(post1, post2, threshold):
    '''
    Takes two Redit posts as inputs.
    Returns true if the posts have the same author and content, regardless of the title.
    This implements Rule 8.
    '''
    author1 = post1.author
    author2 = post2.author
    if author1 == author2 and similar_content(post1, post2, threshold):
        return True
    else:
        return False

# some rules with media (links) involved

# any text with different media is different
# determines if two posts have different media
# same media might have different links - must account for this later
# this slows down stuff and should maybe not always be used

# How to handle false links?
def same_media(post1, post2):
    '''
    Returns true if two posts have the same media or both do not have media, false otherwise.
    Posts have the same media if at least one pair of links in their content lead to the same soure.
    This uses urllib to get what url different links may point to. 
    Every link that is extracted is run through urllib and the resulting links are then pairwise compared.
    If any of the links match, same_media returns true.
    This method may have some potential flaws.
    '''
    links1 = extract_links(post1.content)
    links2 = extract_links(post2.content)
    if links1 == [] and links2 == []:
        return True
    for i in range(len(links1)):
        try:
            with urllib.request.urlopen(links1[i]) as response:
                links1[i] = response.geturl()
        except urllib.error.URLError:
            links1[i] = None
    for i in range(len(links2)):
        try:
            with urllib.request.urlopen(links2[i]) as response:
                links2[i] = response.geturl()
        except urllib.error.URLError:
            links2[i] = None
    for i in links1:
        for j in links2:
            if i == j:
                return True
    return False

# any text retweeting to different thing is different
def same_retweet(post1, post2):
    '''
    Returns true if two posts have the same retweet, false if they are not retweets or do not have the same retweet.
    Currently, extract_retweet only returns the user a user is retweeting.
    '''
    if extract_retweet(post1.content) == extract_retweet(post2.content) and extract_retweet(post1.content) != []: 
        return True
    else:
        return False

# compare content
# all rules for comparing content should also be done to compare name and content of two posts 
# this is only used when one post is from reddit and the other post is from a different platform
# may be problems because different platforms have special text (mastodon has html stuff, twitter has its retweets, different ways of putting in links)

# how to deal with retweets?

# perhaps define function to take function and give cross function

def identical_cross(post1, post2):
    '''
    Returns true if a Reddit post's name and another platform's post's content are identical, false otherwise.
    Alongside similar_cross, this implements Rule 9
    '''
    if post1.name != None:
        if post1.name == post2.content:
            return True
    elif post2.name != None:
        if post2.name == post1.content:
            return True
    return False

def similar_cross(post1, post2, threshold):
    '''
    Returns true if a Reddit post's name and another platform's post's content are similar to a certain threshold, false otherwise.
    Alongside identical_cross, this implements Rule 9.
    '''
    if post1.name != None:
        name = process(post1.name)[0]
        content = process(post2.content)[0]
    elif post2.name != None:
        name = process(post2.name)[0]
        content = process(post1.content)[0]
    else:
        return None
    similarity = SequenceMatcher(None, name, content).ratio()
    if similarity >= threshold:
        return True
    else:
        return False

# probably modify code so this only processes content.
# links and retweet tags can be extracted independently.
def process(content):
    '''
    Processes content according to text processing assumptions.
    Returns processed content, a list of extracted links, and a list of extracted retweet tags.
    Links are extracted and put into list and are then removed from content.
    Tweet tags are extracted and put into list and are then removed from content.
    Content is converted from html2text.
    All whitespace is removed and content is made lower case.
    All duplicate checker functions, asides from ones that check for identical text, work on processed text.
    '''
    if content == "":
        return content, [], [] # this is added because of html2text funky thing
    else:
        links = extract_links(content)
        content = html2text(content)  # this adds two empty lines to "" for some reason so processed "" gets "\n\n"
        content = remove_links(content)
        retweet = extract_retweet(content)
        content = remove_retweet(content)
        content = remove_whitespace(content) # SequenceMatcher counts these whitespaces as differences, should I keep this? - also could have list of words
        content = content.lower()
        return content, links, retweet

def remove_whitespace(content: str) -> str:
    '''
    Removes all whitespace from a string and returns the modified string.
    '''
    return content.replace(' ', '')

# def remove_links(content) -> str:
#     return re.sub('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', '', content)

# regex rule should be modified to check that links are valid
def remove_links(content : str) -> str:
    '''
    Removes all links from a string using regex and returns the modified string.
    '''
    return re.sub('http://\S+|https://\S+', '', content)

# def extract_links(content) -> list[str]:
#     return re.findall('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', content)

def extract_links(content: str) -> list[str]:
    '''
    Puts all links from a string into a list using regex and returns the list.
    This does not modify the string.
    '''
    return re.findall('http://\S+|https://\S+', content)

def remove_retweet(content):
    '''
    Removes all retweet tags from a string using regex and returns the modified string.
    '''
    return re.sub('RT+ @[A-Za-z]+:', '', content)

def extract_retweet(content):
    '''
    Puts all retweets from a string into a list using regex and returns the list.
    This does not modify the string.
    '''
    return re.findall('RT+ @[A-Za-z]+:', content)

def check_links(url1, url2):
    '''
    Returns true if two links lead to the same link, false otherwise.
    Uses urllib to determine where different looking links may lead.
    This function is not used elsewhere.
    '''
    with urllib.request.urlopen(url1) as response:
        u1 = response.geturl() # returns url that url1 directs to
    with urllib.request.urlopen(url2) as response:
        u2 = response.geturl()
    if u1 == u2:
        return True
    else:
        return False


# maybe add more to remove special characters

if __name__ == "__main__":  
    print(process("""RT @KateEBrandt: 🗣️ @Google is helping make information more accessible for everyone – that’s why our free carbon emissions data platform,…"""))
    


# possible casing rules
# I believe that these may be useful for shorter posts but are not for longer ones
# regular to upper or random: not duplicate
# regular to lower: duplicate
# upper to regular, lower, or random: not duplicate
# lower to regular: duplicate
# lower to upper or random: not duplicate
# another rule: whitespace doesn't matter, so same post with different whitespace is duplicate

# possible rule
# using cross but within reddit