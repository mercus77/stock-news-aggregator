# stock_price_fetcher.py
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

class StockPriceFetcher:
    def get_stock_info(self, symbol):
        """Get current stock price and basic info"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                'change': info.get('regularMarketChange', 'N/A'),
                'change_percent': info.get('regularMarketChangePercent', 'N/A'),
                'currency': info.get('currency', 'USD'),
                'logo_url': info.get('logo_url', '')
            }
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return {
                'symbol': symbol,
                'name': symbol,
                'price': 'N/A',
                'change': 'N/A',
                'change_percent': 'N/A',
                'currency': 'USD',
                'logo_url': ''
            }
    
    def get_stock_chart(self, symbol, days=30):
        """Generate interactive price chart"""
        try:
            stock = yf.Ticker(symbol)
            
            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            hist = stock.history(start=start_date, end=end_date)
            
            if hist.empty:
                return None
            
            # Create candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=symbol
            )])
            
            fig.update_layout(
                title=f'{symbol} Price Chart ({days} days)',
                yaxis_title='Price',
                xaxis_title='Date',
                template='plotly_white',
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis_rangeslider_visible=False
            )
            
            return fig.to_html(full_html=False, include_plotlyjs='cdn')
            
        except Exception as e:
            print(f"Error generating chart: {e}")
            return None