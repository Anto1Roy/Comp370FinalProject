import os
import pandas as pd
from itertools import combinations
from math import factorial


def compute_score(row):
    # Count the number of non-empty elements in the row
    non_empty_count = sum(1 for value in row[1:] if not value.empty)

    expected_agreements = factorial(non_empty_count) / (2 * factorial(non_empty_count - 2)) if non_empty_count > 1 else 0
    agreements = 0
    values = {}
    for _, value in row[1].items():
        if value != '':
            if value in values:
                agreements += values[value]
                values[value] += 1
            else:
                values[value] = 1

    return agreements, expected_agreements

def analyze_agreements(df):

    # Compute agreements and expected agreements for each row
    agreements = []
    expected_agreements = []
    for row in df.iterrows():
        agreement, expected_agreement = compute_score(row)
        agreements.append(agreement)
        expected_agreements.append(expected_agreement)

    count_agreements = float(sum(agreements))
    count_expected_agreements = float(sum(expected_agreements))
    print(count_agreements, count_expected_agreements)
    return float((count_agreements - count_expected_agreements) / (1 - count_expected_agreements))

if __name__ == "__main__":
    # Replace 'your_input_file.csv' with your actual file name
    input_file = os.path.join(os.path.dirname(__file__), '../data/articles/results/results.csv')

    # Load responses from CSV
    df = pd.read_csv(input_file)

    # Analyze agreements and compute expected agreements
    print(analyze_agreements(df))
