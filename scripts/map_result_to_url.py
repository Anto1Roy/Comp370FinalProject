import os
import numpy as np
import pandas as pd

def create_mapping_dict(csv_file):
    df = pd.read_csv(csv_file)
    mapping_dict = dict(zip(df['url'], df['coverage']))
    return mapping_dict

def update_second_csv(input_csv, mapping_dict):
    df = pd.read_csv(input_csv)

    # Assuming 'url' column already exists in the second CSV
    list = [''] * 500
    for url in mapping_dict.keys():
        index = df[df['url'] == url].index[0]
        print(index, url, mapping_dict[url])
        list[index] = mapping_dict[url]
    df['ethan'] = list

    # Write the updated DataFrame to the output CSV
    df.to_csv(input_csv, index=False)

if __name__ == "__main__":
    # Replace 'first_csv.csv' and 'second_csv.csv' with your actual file names
    first_csv_file = os.path.join(os.path.dirname(__file__), '../data/articles/articles_both_annotation.csv')
    second_csv_file = os.path.join(os.path.dirname(__file__), '../data/articles/results.csv')

    # Create mapping dictionary
    mapping_dict = create_mapping_dict(first_csv_file)

    # Update the second CSV file with 'ethan' column
    update_second_csv(second_csv_file, mapping_dict)
