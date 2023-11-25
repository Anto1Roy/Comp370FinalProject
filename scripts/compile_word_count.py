import json
import pandas as pd

def count_words(df):
    word_dict = {}
    for i in range(len(df)):
        words = df['description'][i].split()
        # it is in utf-8 format
        words = [word.strip('.,!;()[]{}') for word in words]
        for word in words:
            word = word.lower()
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    return word_dict

def main():
    df = pd.read_csv('/home/nemo/repos/ethann-github/Comp370FinalProject/data/articles/articles_FIX.csv')
    categories = df['category1'].unique()
    word_count = {}
    for category in categories:
        df_category = df[df['category1'] == category].reset_index(drop=True)
        word_dict = count_words(df_category)
        word_count[category] = word_dict
    with open(f'/home/nemo/repos/ethann-github/Comp370FinalProject/data/articles/word_count.json', 'w') as fp:
            json.dump(word_count, fp,indent=4)
       
if __name__ == "__main__":
    main()