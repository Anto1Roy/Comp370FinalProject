import requests
import json
import argparse
from pathlib import Path
import pandas as pd

def fetch_articles(page):
    base_url = 'https://newsapi.org/v2/everything'

    sources_id = json.load(open(Path(__file__).parent.parent / 'data/news_source/sources_id.json', 'r'))['id']
    query_params = {
        'apiKey': args.api_key,
        'sources': ",".join(map(str, sources_id)),
        'q': 'taylor swift',
        'language': 'en',
        'page': page
    }

    source_path = Path(__file__).parent.parent / f'data/articles/cache/articles_{page}.json'
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
    articles = []
    for page in range(1, 6):
        response = fetch_articles(page)
        articles += response['articles']

    for i in articles:
        i['source'] = i['source']['name']
        del i['content']
        del i['urlToImage']
        del i['publishedAt']
    df = pd.DataFrame(articles)
    df['category'] = ''
    df['coverage'] = ''
    df.to_csv(Path(__file__).parent.parent / 'data/articles/articles.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='Your NewsAPI key')
    args = parser.parse_args()
    main()
