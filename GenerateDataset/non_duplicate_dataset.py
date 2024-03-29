# creates non duplicate dataset and exports as csv
# uses dataset containing pulled posts and arranges them into new dataset by containing random pairs

import pandas as pd
import pickle
# the below is need for the pickled dataframe to properly load as it contains the Post class
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open("/Users/cullen/Desktop/Gobo/Datasets/posts.pickle", "rb") as file:
 df = pickle.load(file)

# shuffles df, reset_index(drop=True) makes it so indexes don't shuffle, however unnamed column shuffles, that's okay for now
# see this if we wish to remove: https://stackoverflow.com/questions/43983622/remove-unnamed-columns-in-pandas-dataframe
df2 = df.sample(frac=1).reset_index(drop=True)
df2.rename(columns={"name1": "name2", "content1": "content2", "author1": "author2", "uri1": "uri2", "Object1": "Object2"}, inplace=True)

dataset = pd.concat([df, df2], axis=1)

dataset["duplicate"] = [False for i in range(len(dataset.index))]

with open('/Users/cullen/Desktop/Gobo/Datasets/dataset_nondup.pickle', 'wb') as file:
    pickle.dump(dataset, file)

dataset.to_csv('/Users/cullen/Desktop/Gobo/Datasets/dataset_nonduplicates.csv')

# not sure why I wrote this below, i'll keep it in for now
with open('real_dataset.pickle', 'wb') as file:
    pickle.dump(dataset, file)

