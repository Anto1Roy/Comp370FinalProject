import requests
import json
import argparse
from pathlib import Path
import pandas as pd

def fetch_articles():
    base_url = 'https://newsapi.org/v2/everything'

    sources_id = json.load(open(Path(__file__).parent.parent / 'data/news_source/sources_id.json', 'r'))['id'][:20]
    query_params = {
        'apiKey': args.api_key,
        'sources': ",".join(map(str, sources_id)),
        'q': 'taylor swift',
        'language': 'en',
    }

    source_path = Path(__file__).parent.parent / 'data/articles/cache/articles.json'
    if not source_path.exists():
        try:
            response = requests.get(base_url, params=query_params)
            response.raise_for_status()
            articles_data = response.json()
            with open(source_path, 'w') as f:
                json.dump(articles_data, f)
            return(articles_data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
    else:
        return(json.load(open(source_path, 'r')))

def main():
    articles = fetch_articles()["articles"]
    for i in articles:
        i['source'] = i['source']['name']
        del i['content']
    df = pd.DataFrame(articles)
    df.to_csv(Path(__file__).parent.parent / 'data/articles/articles.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='Your NewsAPI key')
    args = parser.parse_args()
    main()
