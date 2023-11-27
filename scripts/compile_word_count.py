import json
import pandas as pd
import os

def getPath(file):
    return os.path.join(os.path.dirname(__file__), file)

def count_words(df,column):
    word_dict = {}
    for i in range(len(df)):
        words = df[column][i].split()
        # it is in utf-8 format
        words = [word.strip('.,!;()[]{}') for word in words]
        for word in words:
            word = word.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    return word_dict

def removeWords(words_dict):
    words_dict_copy = words_dict.copy()
    for word in words_dict_copy:
        if words_dict[word] < 3:
            words_dict.pop(word)
    return words_dict

def cleanDialog(df):
    # remove stop words
    with open('/home/nemo/repos/ethann-github/Comp370FinalProject/data/stopwords.txt','r') as f:
        stop_words = f.read().splitlines()
        # print(stop_words)
    df['description'] = df['description'].apply(lambda x: ' '.join([word.lower() for word in x.split() if word.lower() not in stop_words]))
    df['title'] = df['title'].apply(lambda x: ' '.join([word.lower() for word in x.split() if word.lower() not in stop_words]))
    
    return df
    
def main():
    fn = getPath('../data/articles/articles_FIX.csv')
    df = pd.read_csv(fn)
    categories = df['category1'].unique()
    df = cleanDialog(df)
    word_count = {}
    for category in categories:
        df_category = df[df['category1'] == category].reset_index(drop=True)
        title_word_dict = count_words(df_category,"title")
        description_word_dict = count_words(df_category,"description")
        description_word_dict.update(title_word_dict)
        description_word_dict = removeWords(description_word_dict)
        # combine two dicts
        word_count[category] = description_word_dict
    
    fnWordCount = getPath('../data/articles/word_count.json')
    with open(fnWordCount, 'w') as fp:
        json.dump(word_count, fp,indent=4)
if __name__ == "__main__":
    main()