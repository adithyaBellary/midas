from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta, date, time
import os
import pandas as pd

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame

load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

LIMIT = 1000
def generate():
  if os.environ.get('PAPER') == 'TRUE':
    key_id = PAPER_KEY_ID
    secret_key = PAPER_SECRET_KEY
    url = PAPER_URL
  else :
    key_id = KEY_ID
    secret_key = ALPACA_SECRET_KEY
    url = URL


  api = tradeapi.REST(
    key_id=key_id,
    secret_key=secret_key,
    base_url=url,
    api_version= 'v2'
  )

  for index, day in enumerate([datetime.today() - timedelta(days=x) for x in range(2,202)]):

    d_bars = api.get_bars(
      'AAPL',
      TimeFrame.Minute,
      day.strftime("%Y-%m-%d"),
      day.strftime("%Y-%m-%d"),
      limit=LIMIT,
      adjustment='raw'
    ).df

    d_bars.to_csv('data/test.csv', mode='a', header=index == 0)
