import pickle
from update_dataset_helper import modify_post, add_data

with open('/Users/cullen/Desktop/Gobo/Datasets/dataset_nondup.pickle', 'rb') as file:
    df = pickle.load(file) 

# rules for reference
# General Rules
# Rule 1: Two posts have identical content
# Rule 2: Two posts have very similar text and the same media or no media (see non duplicate assumptions 1 and 2)
# Rule 3: Two posts have very similar text and are retweeting to the same tweet (PROBLEM: regex only checks retweeting same user) or not retweeting

# Two Reddit Post Rules (NEEDS MORE THOUGHT)
# Rule 4: Two Reddit posts have identical names and content (does name matter at all here, in this case it need not be explicitly coded) (no media)
# Rule 5: Two Reddit posts have very similar names and content (no media)
# ? Rule 6: Two Reddit posts have identical or very similar names (but what if content is different - perhaps sufficiently similar content)
# ? Rule 7: Two Reddit posts have identical or very similar content (this is covered in rules 1-2, does name matter at all here?)
# Rule 8: Two Reddit posts have the same author and identical or very similar content, regardless of the name.

# One Reddit Post, One Not Rules (Needs more thought, see in wild)
# Rule 9: A Reddit Post name and a non Reddit Post content are similar according to Rules 1-3 (what about content of Reddit post, also media considerations)
# Rule 10: A Reddit Post and non Reddit post have identical or very similar content. (covered in Rules 1-3) (what about name of Reddit post? media)

# Non Duplicate Assumptions (some intricacies may be added here)
# 1 - Two posts that share different media are not duplicates, regardless of text
# 2 - Two posts that are retweeting to different tweets are not duplicates, regardless of text

# Text Processing Assumptions - Content and Names are processed according to the following assumptions.
# 1 - Casing does not matter. All text is converted to lower case for comparison.
# 2 - Whitespace does not matter. Whitespace is removed from text.
# 3 - Special characters do not matter. Special characters are removed from text (not implemented yet)
# 4 - Html text may be converted to regular text by removing all tags.
# 5 - Links and retweet tags do not matter. They are removed from the text and may be used in comparing media or retweet tags.
# 6 - All of these above rules can be used to process any text before it is compared (maybe some exceptions should be allowed)


# Rule 1 - identical duplicates
add_data(df, 0, df["Object1"][0]) # Reddit post about joe west
add_data(df, 30, df["Object1"][30]) # Twitter post about turkish president
add_data(df, 60, df["Object1"][60]) # Mastodon post from Nasa

# Rule 2 - very similar text with same media
# Case 1 - All cap
add_data(df, 37, modify_post(df["Object1"][37], "Do you ever see faces in things? That's a phenomenon called pareidolia, and it's when our brains see familiar shapes in objects or data, like in the cloud clouds or the cosmos. Here are some of our favorite examples of pareidolia in space:".upper() + " https://t.co/kwBzhkEYCo https://t.co/onp5BdTuUf"))
print(df.iloc[len(df.index)-1])

# Case 2 - Lower case
add_data(df, 37, modify_post(df["Object1"][37], "Do you ever see faces in things? That's a phenomenon called pareidolia, and it's when our brains see familiar shapes in objects or data, like in the cloud clouds or the cosmos. Here are some of our favorite examples of pareidolia in space:".upper() + " https://t.co/kwBzhkEYCo https://t.co/onp5BdTuUf"))
print(df.iloc[len(df.index)-1])

# Case 3 - No spaces
add_data(df, 37, modify_post(df["Object1"][37], "Do you ever see faces in things? That's a phenomenon called pareidolia, and it's when our brains see familiar shapes in objects or data, like in the cloud clouds or the cosmos. Here are some of our favorite examples of pareidolia in space:".replace(" ", "") + " https://t.co/kwBzhkEYCo https://t.co/onp5BdTuUf"))
print(df.iloc[len(df.index)-1])

# Case 4 - Extra white space
add_data(df, 37, modify_post(df["Object1"][37], "          Do you ever   see faces in things?   That's a phenomenon called    pareidolia, and it's when our brains        see familiar   shapes in objects           or data, like in the        cloud clouds or the cosmos. Here are some of our favorite     examples of pareidolia in space: https://t.co/kwBzhkEYCo https://t.co/onp5BdTuUf             "))
print(df.iloc[len(df.index)-1])

# Case 5 - Typos
add_data(df, 37, modify_post(df["Object1"][37], "Do u ever see faves in things? That is a phenomenen called paredolia, and it is when our brainsj see familuar shapes in objecstsa or data like in the clouds or the kosmosa Here's some of our favoriteas exampkes of pareidolia  in space: https://t.co/kwBzhkEYCo https://t.co/onp5BdTuUf"))
print(df.iloc[len(df.index)-1])

# Case 6 - Html vs no html, different links lead to same place (Twitter Mastodon Comparison)
add_data(df, 37, df["Object1"][62])
print(df.iloc[len(df.index)-1])

# Non duplicate Case 1 - Different media (I just removed the link here)
add_data(df, 37, modify_post(df["Object1"][37], "Do you ever see faces in things? That's a phenomenon called pareidolia, and it's when our brains see familiar shapes in objects or data, like in the cloud clouds or the cosmos. Here are some of our favorite examples of pareidolia in space"), False)
print(df.iloc[len(df.index)-1])

with open('/Users/cullen/Desktop/Gobo/Datasets/complete_dataset.pickle', 'wb') as file:
    pickle.dump(df, file)

df.to_csv('/Users/cullen/Desktop/Gobo/Datasets/complete_dataset.csv')