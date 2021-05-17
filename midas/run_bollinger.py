from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
import alpaca_trade_api as tradeapi

from services import test_suite
from tradeModels.bollinger import BollingerModel

load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

FILE_NAME = 'bollinger_test'
NUM_DAYS = 1

WINDOW = 10
# number of minute intervals
TIME_STEP = 1
BOLLINGER_BAND_1_MULTIPLIER = 1
BOLLINGER_BAND_2_MULTIPLIER = 2


def main():

  # let us generate some data
  test_suite.generate(
    'AAPL',
    FILE_NAME,
    NUM_DAYS
  )
  # now let us read this back
  csv_data = pd.read_csv(f'data/{FILE_NAME}.csv')

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
    api_version='v2'
  )

  bollinger = BollingerModel(
    WINDOW,
    TIME_STEP,
    BOLLINGER_BAND_1_MULTIPLIER,
    BOLLINGER_BAND_2_MULTIPLIER,
    api
  )

  # iterate through the numpy array
  for index, row in csv_data.iterrows():
    # print(row['open'])
    bollinger.on_bar(row)
    # pass


if __name__ == "__main__":
  main()