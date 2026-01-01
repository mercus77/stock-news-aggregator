# news_fetcher.py
import requests
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_stock_news(self, stock_symbol, company_name, days_back=7):
        """Fetch news for a specific stock with date filtering"""
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        params = {
            'q': f'{company_name} OR {stock_symbol}',
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': self.api_key,
            'pageSize': 20,
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                return self.format_articles(data['articles'])
            else:
                return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def fetch_multiple_stocks_news(self, stock_symbols, days_back=7):
        """Fetch news for multiple stocks"""
        all_articles = []
        
        for symbol in stock_symbols:
            articles = self.fetch_stock_news(symbol, symbol, days_back)
            for article in articles:
                article['related_stock'] = symbol
            all_articles.extend(articles)
        
        # Sort by date
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        
        return all_articles
    
    def format_articles(self, articles):
        """Format articles for display"""
        formatted = []
        for article in articles:
            formatted.append({
                'title': article['title'],
                'source': article['source']['name'],
                'published': article['publishedAt'],
                'url': article['url'],
                'description': article.get('description', 'No description available')
            })
        return formatted