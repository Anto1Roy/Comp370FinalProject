import csv
import math
import os
import pandas as pd
from itertools import combinations
from math import factorial


def compute_score(row):
    agreements = 0
    non_empty_count = 0
    values = {}
    for value in row[1:]:
        value = value.lower().strip()
        if value != "":
            non_empty_count += 1
            if value in values:
                agreements += values[value]
                values[value] += 1
            else:
                values[value] = 1

    if non_empty_count > 1:
        expected_agreements = calculate_pairs_and_combinations(non_empty_count)
    else:
        expected_agreements = 0

    return agreements, expected_agreements


def calculate_pairs_and_combinations(n):
    # Calculate the total number of pairs
    total_pairs = 3 + 3 * math.comb(n, 2) + 3**n - 3 - math.comb(n, 2)

    # Calculate the total number of combinations
    total_combinations = 3**n

    # Calculate the result by dividing the number of pairs by the number of combinations
    result = total_pairs / total_combinations

    return result


def analyze_agreements(file):
    with open(input_file, "r") as file:
        # Assuming the first row contains headers, and the remaining rows contain data
        reader = csv.reader(file)

        # Compute agreements and expected agreements for each row
        agreements = []
        expected_agreements = []
        for row in reader:
            agreement, expected_agreement = compute_score(row)
            agreements.append(agreement)
            expected_agreements.append(expected_agreement)

    # print(expected_agreements)
    count_agreements = float(sum(agreements))
    count_expected_agreements = float(sum(expected_agreements))
    print(count_agreements, count_expected_agreements)

    P_o = count_agreements / (count_agreements + count_expected_agreements)
    P_e = (
        (
            (count_agreements + count_expected_agreements)
            * (count_agreements + count_expected_agreements)
        )
        + (count_agreements * count_expected_agreements)
    ) / ((2 * count_agreements + count_expected_agreements) ** 2)

    # Calculate Cohen's Kappa
    kappa = (P_o - P_e) / (1 - P_e)

    return kappa


if __name__ == "__main__":
    input_file = os.path.join(
        os.path.dirname(__file__), "../data/articles/results/results.csv"
    )

    # Analyze agreements and compute expected agreements
    print(analyze_agreements(input_file))
