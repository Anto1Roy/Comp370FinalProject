import json
import os
import pandas as pd

def analyze_csv(input_csv, output_json):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)

    # Convert 'score' column to numeric (assuming it contains numeric values)
    df['score'] = pd.to_numeric(df['score'], errors='coerce')

    # Compute average score and standard deviation for each category
    #group_stats = df.groupby('category')['score'].agg(['mean', 'std', 'avg']).reset_index()
    group_stats = df['score'].agg(['mean', 'std'])

    # Convert group_stats DataFrame to a dictionary for JSON output
    stats_dict = group_stats.to_dict()

    # Save the results to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(stats_dict, json_file, indent=2)

if __name__ == "__main__":
    # Replace 'your_input_file.csv' and 'output_stats.json' with your actual file names
    input_file = os.path.join(os.path.dirname(__file__), '../data/articles/articles.csv')
    output_json = os.path.join(os.path.dirname(__file__), '../data/articles/results/stats_overall.json')

    # Analyze the CSV file and save results to JSON
    analyze_csv(input_file, output_json)
