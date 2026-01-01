# app.py
from news_fetcher import NewsFetcher
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Get API key from environment variable
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("Please set NEWS_API_KEY in your .env file")
        return
    
    fetcher = NewsFetcher(api_key)
    
    print("=" * 80)
    print("Welcome to Stock News Aggregator!")
    print("=" * 80)
    
    while True:
        print("\nEnter a stock symbol (or 'quit' to exit):")
        stock_symbol = input("> ").strip().upper()
        
        if stock_symbol == 'QUIT':
            print("Thanks for using Stock News Aggregator! Goodbye!")
            break
        
        if not stock_symbol:
            print("Please enter a valid stock symbol.")
            continue
        
        print(f"\nFetching news for {stock_symbol}...\n")
        articles = fetcher.fetch_stock_news(stock_symbol, stock_symbol)
        
        # Display the news
        if articles:
            print(f"Found {len(articles)} articles:\n")
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Published: {article['published']}")
                print(f"   URL: {article['url']}")
                if article['description']:
                    desc = article['description'][:150]
                    print(f"   {desc}...")
                print("-" * 80)
        else:
            print(f"No articles found for {stock_symbol}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

