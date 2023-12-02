import csv
import os

def compute_score(row):
    # Count the number of non-empty elements in the row
    non_empty_count = sum(1 for value in row[1:] if value.strip() != '')

    # Calculate the score based on the rules provided
    score = sum(1 if value.lower().strip() == 'positive' else -1 if value.lower().strip() == 'negative' else 0
                for value in row[1:]) / non_empty_count if non_empty_count > 0 else 0

    return score

def main(input_file):
    with open(input_file, 'r') as file:
        # Assuming the first row contains headers, and the remaining rows contain data
        reader = csv.reader(file)
        
        # Compute scores for each URL
        scores = {}
        for row in reader:
            url = row[0]
            score = compute_score(row)
            scores[url] = score
            print(f"{url}: {score}")


if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), '../data/articles/results/results.csv')  # Replace with the actual CSV file path
    main(input_file)
