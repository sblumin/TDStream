import os
from dotenv import load_dotenv
from td.client import TDClient
import pandas as pd

# Get list of S&P 500 symbols
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df = df['Symbol']
sp_list = df.values.tolist()

# Add any stocks not in S&P 500
check = set(sp_list)
f = open("stocks.txt", "r")
for sym in f:
  if sym not in check:
    sp_list.append(sym)
    check.add(sym)

# Load environment variables holding key and callback url
load_dotenv()
key = os.environ.get('CONSUMER_KEY')
url = os.environ.get('CALLBACK_URL')
credentials_path = 'C:\\Users\\austi\\credentials\\td_state.json'

# Instantiate TDClient and login
td_session = TDClient(client_id=key, redirect_uri=url, credentials_path=credentials_path)
td_session.login()

# Set up streaming
td_streamer = td_session.create_streaming_session()

# Direct streamer to write data to specified file path
td_streamer.write_behavior(file_path='level_one_quotes_data.csv')

# Subscribe to level one quotes
options_fields = [0, 1, 2, 3, 4, 5, 8, 24]
td_streamer.level_one_quotes(symbols=sp_list, fields=options_fields)

# Subscribe to timesale data
timesale_fields = [0, 1, 2, 3, 4]
td_streamer.timesale(service='TIMESALE_EQUITY', symbols=sp_list, fields=timesale_fields)

# Stream
td_streamer.stream()
