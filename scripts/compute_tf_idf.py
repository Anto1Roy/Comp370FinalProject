import pandas as pd
import json 
import math
import os

def tf(category,word,word_count):
    return word_count[category][word]

def idf(word,word_count):
    num_categories = len(word_count)
    num_categories_with_word = 0
    for category in word_count:
        if word in word_count[category]:
            num_categories_with_word += 1
    idf = math.log(num_categories/num_categories_with_word)
    return idf
def compute_tf_idf(word, category, word_count):
    tfidf_dict = {}
    for category in word_count:
        tfidf_dict[category] = {}
        for word in word_count[category]:
            tfidf_dict[category][word] = tf(category,word,word_count)*idf(word,word_count)
    return tfidf_dict

def main():
    df = pd.read_csv('/home/nemo/repos/ethann-github/Comp370FinalProject/data/articles/articles_FIX.csv')
    # create a new csv for each categories
    with open(f'/home/nemo/repos/ethann-github/Comp370FinalProject/data/articles/word_count.json', 'r') as fp:
        word_count = json.load(fp)
    tfidf = {}
    for category in word_count:
        word_dict = word_count[category]
        tfidf = compute_tf_idf(word_dict,category,word_count)

    with open(f'/home/nemo/repos/ethann-github/Comp370FinalProject/data/articles/tfidf.json', 'w') as fp:
        json.dump(tfidf, fp,indent=4)
if __name__ == "__main__":
    main()