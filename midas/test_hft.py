from alpaca_trade_api.stream import Stream
import pandas as pd
import numpy as np
import time
import logging
import asyncio
import threading
from dotenv import load_dotenv, find_dotenv
import sys
import os
import django

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL as alpacaURL

from tradeModels import ScalpModel as scalpModel

load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

async def print_trade(t):
	print('trade', t)

async def print_quote(q):
	print('quote', q)

async def on_bar(b):
	print('bar', b)

async def on_trade_update(tu):
	print('on trade update', tu)

async def on_status_update(su):
	print('on status update', su)

def run():
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
		base_url=alpacaURL(url),
		api_version= 'v2'
	)

	# Establish streaming connection

	# track our buying power
	account = api.get_account()
	buying_power = account.buying_power
	print('buying power', buying_power)

	feed = 'iex'
	stream = tradeapi.Stream(
		key_id=key_id,
		secret_key=secret_key,
		data_feed=feed,
		base_url=alpacaURL(url),
		raw_data=True
	)

	stream.subscribe_trades(print_trade, 'AAPL')
	stream.subscribe_quotes(print_quote, 'SPOT')
	stream.subscribe_bars(on_bar, 'AAPL')
	stream.subscribe_trade_updates(on_trade_update)
	stream.subscribe_statuses(on_status_update, 'AAPL')

def run_hft():
	run()
