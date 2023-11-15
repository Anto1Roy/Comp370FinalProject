import json
import requests
import argparse
from pathlib import Path


def fetch_sources(country):
    base_url = 'https://newsapi.org/v2/top-headlines/sources'

    query_params = {
        'apiKey': args.api_key,
        'language': 'en',
        'country': country
    }

    
    source_path = Path(__file__).parent.parent / f'data/news_source/cache/{country}.json'

    if not source_path.exists():
        try:
            response = requests.get(base_url, params=query_params)
            response.raise_for_status()
            sources_data = response.json()
            with open(source_path, 'w') as f:
                json.dump(sources_data, f)
            return(sources_data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
    else:
        return(json.load(open(source_path, 'r')))

def main():
    us_sources = fetch_sources('us')
    canada_sources = fetch_sources('ca')    
    # sources_list.md should not be overwritten once generated 
    ''' 
    with open(Path(__file__).parent.parent / 'data/news_source/sources_list.md', 'w') as f:
        for i in canada_sources['sources']:
            f.write(i['name'] + '\n')
        for i in us_sources['sources']:
            f.write(i['name'] + '\n')
    '''
    
    # generate sources_id.json which is a list of all the sources' id
    with open(Path(__file__).parent.parent / 'data/news_source/sources_id.json', 'w') as f:
        ids = {"id" : []}
        for i in canada_sources['sources']:
            ids['id'].append(i['id'])

        for i in us_sources['sources']:
            ids['id'].append(i['id'])
        json.dump(ids, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('api_key', help='Your NewsAPI key')
    args = parser.parse_args()
    main()