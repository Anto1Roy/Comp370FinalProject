import json
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_text_elements(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all <p> tags containing the keyword
            paragraphs = soup.find_all('p', string=lambda text: 'taylor swift' or 'swift' in text.lower())
            
            # Extract the text from each matching <p> tag
            return [paragraph.get_text() for paragraph in paragraphs]

        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    
    # Read the CSV file using pandas
    csv_file_path = Path(__file__).parent.parent.parent / 'data/articles/articles.csv' # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)

    # List of URLs to scrape
    url_list = df['url']

    data_dict = {}

    # Loop through each URL and scrape text elements
    for url in url_list:
        print(f"Scraping {url}...")
        # Store the data in the dictionary
        data_dict[url] = {
            'paragraphs' : scrape_text_elements(url)
        }

    # Write the data to a JSON file
    output_file_path = Path(__file__).parent.parent.parent / 'data/articles/content.json'
    with open(output_file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=2)

    print(f"Data has been written to {output_file_path}")

