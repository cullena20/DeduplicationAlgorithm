# need better names for these functions, they also could use more functionality

import pickle
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from duplicate_checker import is_duplicate
from duplicate_checker import is_duplicate_dict
from duplicate_checker import process

with open("/Users/cullen/Desktop/Gobo/Datasets/dataset_nondup.pickle", "rb") as file:
 df = pickle.load(file)

with open("/Users/cullen/Desktop/Gobo/Datasets/dup_dataset.pickle", "rb") as file:
 df2 = pickle.load(file)

def check_duplicates(df: pd.DataFrame) -> list[bool]:
    '''
    Uses the duplicate checker algorithm to check for duplicates in the dataset.
    Results is a list of boolean values containing what our algorithm predicts the pair to be.
    This code does not compare the algorithm's predictions with their true values.
    '''
    results = [is_duplicate(df["Object1"][idx], df["Object2"][idx]) for idx in df.index]
    return results

def display_results(results: list[bool]):
    '''
    Displays the predictions made by the duplicate checker algorithm.
    This prints out what the algorithm expects, not the true values.
    '''
    print(f"Total: {len(results)}")
    print(f"Duplicates: {results.count(True)}")
    print(f"Non-Duplicates: {results.count(False)}")
    
def display_incorrect(df, test_results):
    '''
    Prints any pairs of posts that the algorithm incorrectly predicts.
    Also prints metrics that algorithm predicts.
    '''
    incorrect_idx = [i for i, j in enumerate(test_results) if j == False]
    for i in incorrect_idx:
        print(f"Entry {i}; " + "Predicted value: " + str(not df["duplicate"][i]) + "; Expected value: " + str(df["duplicate"][i]) + "\n")
        print(df.iloc[i])
        print(is_duplicate_dict(df2["Object1"][i], df2["Object2"][i]))

results = check_duplicates(df2)

display_results(results)
print()

# compares algorithm's predictions to expected results.
# Returns an array where True means the algorithm succesfully worked, and False when it fails
test_results = [(df2["duplicate"][idx] == results[idx]) for idx in df2.index]

print("Accuracy: " + str(test_results.count(True) / len(test_results)))
# print(test_results)
print()

display_incorrect(df2, test_results)

# see this for problems 
print()
print(process(df2["content1"][89])[1])
print(process(df2["content2"][89])[1])

print()

print(df2["content1"][89])
print(df2["content2"][89])


