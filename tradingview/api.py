# import yfinance as yf
# meta = yf.Ticker("META")
# print("Company Sector:", meta.info['sector'])
# print("P/E Ratio:", meta.info['trailingPE'])
# print("Company Beta:", meta.info['beta'])
# print("Market Cap:", meta.info.get('marketCap'))
# print("Event Type:", meta.info.get('eventType'))

import yfinance as yf

symbols = ['META']
data = yf.download(symbols, period='1d')
print(data.info)

# import yfinance as yf
# symbols = ['META', 'GOOGL', 'AAPL', 'MSFT']
# for symbol in symbols:
# 	meta = yf.Ticker(symbol)
# 	for key, value in meta.info.items():
# 	    print(f"{key}: {value}")


# import yfinance as yf
# import pandas as pd

# symbols = ['META', 'GOOGL', 'AAPL', 'MSFT']
# # EVENT_TYPES = (("earnings", 'Earnings'), ("split", 'Split'), ("fork", 'Fork'), ("other", 'Other'))
# # IMPACT_LEVELS = (("low", 'Low'), ("medium", 'Medium'), ("high", 'High'))
# for symbol in symbols:
# 	meta = yf.Ticker(symbol)
# 	for key, value in meta.calendar.items():
# 		if 'Earnings' in key:
# 			title = f"{symbol} Earnings"
# 			date = value
# 			if isinstance(date, list):
# 				date = date[0]
# 			else:
# 				date = value
# 			if isinstance(date, pd.Timestamp):
# 				date = date.date()

# 			event_type = "earnings" 
# 			impact_level = "high"
# 			print({title})
# 			print({date})
# 			print({event_type})
# 			print({impact_level})
  
# 	print()

	# print(f"{symbol} earnings_high: {earnings_high}")
	# print(f"{symbol} earnings_low: {earnings_low}")
	# print(f"{symbol} earnings_average: {earnings_average}")
	# print(earnings_date)

	# try:
	#     articles = data[0]
	#     id = article.get('id')
	#     title = article.get('content', {}).get('title')
	#     description = article.get('content', {}).get('description')
	#     summary = article.get('content', {}).get('summary')
	#     published_at = article.get('content', {}).get('pubDate')
	#     link = article.get('content', {}).get('canonicalUrl').get('url')


	#     print(f"ID: {id}")
	#     print(f"Title: {title}")
	#     print(f"Description: {description}")
	#     print(f"Summary: {summary}")
	#     print(f"Published Date: {published_at}")
	#     print(f"Link: {link}")
	# except IndexError:
	#     print("No news available")





	# Simple Moving Averages
    # hist['SMA10'] = hist['Close'].rolling(window=10).mean()
    # hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    # hist['SMA200'] = hist['Close'].rolling(window=200).mean()


# import yfinance as yf

# symbols = ['META', 'GOOGL', 'AAPL', 'MSFT']
# news_data = {}

# for symbol in symbols:
#     meta = yf.Tickers(symbol)
#     news = meta.news()
#     news_data[symbol] = []
#     for article in news:
#         news_data[symbol].append({
#             'title': article.get('title', ''),
#             'publisher': article.get('publisher', ''),
#             'link': article.get('link', ''),
#             'providerPublishTime': article.get('providerPublishTime', ''),
#         })

# print(news_data)
