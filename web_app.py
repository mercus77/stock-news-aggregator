# web_app.py
from flask import Flask, render_template, request, session
from news_fetcher import NewsFetcher
from stock_price_fetcher import StockPriceFetcher
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here-change-this'

api_key = os.getenv('NEWS_API_KEY')
news_fetcher = NewsFetcher(api_key)
price_fetcher = StockPriceFetcher()

@app.route('/')
def home():
    watchlist = session.get('watchlist', [])
    return render_template('index.html', watchlist=watchlist)

@app.route('/search', methods=['POST'])
def search():
    stock_symbol = request.form.get('stock_symbol', '').strip().upper()
    days_back = int(request.form.get('days_back', 7))
    
    watchlist = session.get('watchlist', [])
    
    if not stock_symbol:
        return render_template('index.html', 
                             error="Please enter a stock symbol",
                             watchlist=watchlist)
    
    # Get stock price info
    stock_info = price_fetcher.get_stock_info(stock_symbol)
    
    # Get price chart
    chart_html = price_fetcher.get_stock_chart(stock_symbol, days=30)
    
    # Get news articles
    articles = news_fetcher.fetch_stock_news(stock_symbol, stock_symbol, days_back)
    
    return render_template('index.html', 
                         stock_symbol=stock_symbol,
                         stock_info=stock_info,
                         chart_html=chart_html,
                         articles=articles,
                         days_back=days_back,
                         watchlist=watchlist)

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    stock_symbol = request.form.get('stock_symbol', '').strip().upper()
    
    if stock_symbol:
        watchlist = session.get('watchlist', [])
        if stock_symbol not in watchlist:
            watchlist.append(stock_symbol)
            session['watchlist'] = watchlist
    
    return search()

@app.route('/remove_from_watchlist/<symbol>')
def remove_from_watchlist(symbol):
    watchlist = session.get('watchlist', [])
    if symbol in watchlist:
        watchlist.remove(symbol)
        session['watchlist'] = watchlist
    
    return home()

@app.route('/watchlist_news')
def watchlist_news():
    watchlist = session.get('watchlist', [])
    days_back = int(request.args.get('days_back', 7))
    
    if not watchlist:
        return render_template('index.html', 
                             watchlist=watchlist,
                             error="Your watchlist is empty. Add some stocks first!")
    
    # Get price info for all watchlist stocks
    stocks_info = []
    for symbol in watchlist:
        info = price_fetcher.get_stock_info(symbol)
        stocks_info.append(info)
    
    # Get news for all watchlist stocks
    articles = news_fetcher.fetch_multiple_stocks_news(watchlist, days_back)
    
    return render_template('index.html',
                         watchlist=watchlist,
                         stocks_info=stocks_info,
                         articles=articles,
                         days_back=days_back,
                         viewing_watchlist=True)

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

if __name__ == '__main__':
    app.run(debug=True)