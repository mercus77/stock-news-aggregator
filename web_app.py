@app.route('/search', methods=['GET', 'POST'])
def search():
    # Handle GET vs POST for the symbol
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol', '').strip().upper()
        days_back = int(request.form.get('days_back', 7))
    else:
        stock_symbol = request.args.get('stock_symbol', '').strip().upper()
        days_back = int(request.args.get('days_back', 7))
    
    watchlist = session.get('watchlist', [])
    
    if not stock_symbol:
        return render_template('index.html', error="Please enter a stock symbol", watchlist=watchlist)
    
    # --- SAFETY FIX STARTS HERE ---
    try:
        # 1. Get Stock Info (with safety defaults)
        raw_info = price_fetcher.get_stock_info(stock_symbol)
        
        # Ensure stock_info is a dictionary with at least empty values if keys are missing
        stock_info = {
            'current_price': raw_info.get('current_price', 'N/A') if raw_info else 'N/A',
            'sector': raw_info.get('sector', 'Unknown Sector') if raw_info else 'Unknown',
            'summary': raw_info.get('summary', 'No summary available.') if raw_info else 'No summary available.'
        }
    except Exception as e:
        print(f"Error fetching stock info: {e}")
        stock_info = None

    try:
        # 2. Get Chart
        chart_html = price_fetcher.get_stock_chart(stock_symbol, days=30)
    except Exception as e:
        print(f"Error fetching chart: {e}")
        chart_html = None

    try:
        # 3. Get News
        articles = news_fetcher.fetch_stock_news(stock_symbol, stock_symbol, days_back)
    except Exception as e:
        print(f"Error fetching news: {e}")
        articles = []
    # --- SAFETY FIX ENDS HERE ---

    return render_template('index.html', 
                           stock_symbol=stock_symbol,
                           stock_info=stock_info,
                           chart_html=chart_html,
                           articles=articles,
                           days_back=days_back,
                           watchlist=watchlist)