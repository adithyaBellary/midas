import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL as alpacaURL

from services import test_suite
from tradeModels.ml import MlEngine

load_dotenv(find_dotenv())

STOCK = 'AAPL'
OUTPUT_FILE = 'mock_data'
NUM_TRAINING_DAYS = 100

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

def main():
	if os.environ.get('PAPER') == 'TRUE':
		key_id = PAPER_KEY_ID
		secret_key = PAPER_SECRET_KEY
		url = PAPER_URL
	else:
		key_id = KEY_ID
		secret_key = ALPACA_SECRET_KEY
		url = URL

	api = tradeapi.REST(
		key_id=key_id,
		secret_key=secret_key,
		base_url=alpacaURL(url),
		api_version= 'v2'
	)

	test_suite.generate(
		STOCK,
		OUTPUT_FILE,
		NUM_TRAINING_DAYS
	)

	# load the csv into a local pandas dataframe
	mock_dataframe = pd.read_csv(OUTPUT_FILE)

	engine = MlEngine(
		weight_path='model_300_days_40_epochs.pt',
		alpaca_api=api,
		input_length=25,
		lookahead=10,
		stock='AAPL'
	)

	# some kind of apply function to apply the on bar function to the data frame
	mock_dataframe.apply(engine.on_bar)

if __name__ == "__main__":
	main()