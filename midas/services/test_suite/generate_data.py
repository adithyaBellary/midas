from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta, date, time
import os

import alpaca_trade_api as tradeapi

load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

def generate():

  print('generating')
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

  symbols = ['AAPL']

  d = api.get_aggs(
    'AAPL',
    1,
    'minute',
    '2021-02-01',
    '2021-02-02'
  ).df

  d.to_csv('data/test.csv')
