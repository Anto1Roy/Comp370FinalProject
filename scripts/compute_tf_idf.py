import pandas as pd
import json 
import math
import os

def getPath(file):
    return os.path.join(os.path.dirname(__file__), file)

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
    # create a new csv for each categories
    fnJson = getPath('../data/articles/word_count_all.json')
    with open(fnJson, 'r') as fp:
        word_count = json.load(fp)
    tfidf = {}
    for category in word_count:
        word_dict = word_count[category]
        tfidf = compute_tf_idf(word_dict,category,word_count)

    fntidf = getPath('../data/articles/tfidf.json')
    with open(fntidf, 'w') as fp:
        json.dump(tfidf, fp,indent=4)
if __name__ == "__main__":
    main()