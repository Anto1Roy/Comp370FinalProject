import requests
import json

def fetch_taylor_swift_articles(api_key, num_articles=500):
    # In order to use the specification country, we need to use 'top-headlines/sources' instead of 'everything'
    base_url = 'https://newsapi.org/top-headlines/sources'

    # query params for the us
    query_params = {
        'q': 'Taylor Swift',
        'apiKey': api_key,
        'pageSize': 100,  # News API allows a maximum of 100 results per request
        'language': 'en',  # English language
        "country": "us" # Country
    }
    # query params for canada
    query_params = {
        'q': 'Taylor Swift',
        'apiKey': api_key,
        'pageSize': 100,  # News API allows a maximum of 100 results per request
        'language': 'en',  # English language
        "country": "ca" # Country
    }

    all_articles = []

    # Testing the queries
    for page in range(1, (num_articles // query_params['pageSize']) + 2):
        query_params['page'] = page

        try:
            response = requests.get(base_url, params=query_params)
            response.raise_for_status()
            articles_data = response.json()

            if 'articles' in articles_data:
                all_articles.extend(articles_data['articles'])

            if len(all_articles) >= num_articles:
                break

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
            break

    return all_articles[:num_articles]

def main():
    api_key = 'ee2d01b05edc45cc958bf558eddc3aea'  # Replace with your News API key
    num_articles_to_fetch = 100 # Will be 500+ in the future

    try:
        articles = fetch_taylor_swift_articles(api_key, num_articles_to_fetch)

        for idx, article in enumerate(articles, start=1):
            print(f"{idx}. {article['title']} - {article['url']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
