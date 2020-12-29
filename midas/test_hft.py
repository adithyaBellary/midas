import pandas as pd
import numpy as np
import time
import logging
import asyncio
import threading
from dotenv import load_dotenv, find_dotenv
import sys
import os

import services.alpaca_trade_api as tradeapi
import tradeModels.scalping as scalpModel
from tradeModels.scalping.typedefs import BarTick

load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

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
		base_url=url
	)
	polygon = api.polygon

	# Establish streaming connection

	conn = tradeapi.StreamConn(
		key_id=key_id,
		secret_key=secret_key,
		base_url=url,
		data_stream='polygon',
		debug=True
	)
	# track our buying power
	account = api.get_account()

	model = scalpModel.ScalpModel(
		api=api,
		symbol='AAPL'
	)
	# model.on_bar(tick=BarTick(o=102.3, ticker='AAPL'))
	# model._outOfMarket()
	model.get_olders()
	# model.update_time()

	@conn.on(r'^AM')
	async def on_AM(conn, channel, data):
		print('in AM ', data)

	@conn.on(r'^A$')
	async def on_A(conn, channel, data):
		print('in A$')

	@conn.on(r'^A')
	async def on_A(conn, channel, data):
		print('in A ')

	@conn.on(r'trade_updates')
	async def on_trade_updates(conn, channel, data):
		# We got an update on one of the orders we submitted. We need to
		# update our position with the new information.
		print('in on_trade_updates ', data)

	@conn.on(r'^status')
	async def on_status(conn, channel, data):
		print('channel: {}, data: {}'.format(channel, data))

	# we will need to run the periodic check function with this run Function
	# conn.run([
	# 	'A.AAPL',
	# 	# 'AM.AAPL',
	# 	# 'AM.*',
	# 	'trade_updates',
	# 	'account_updates'
	# ])

def run_hft():
	run()


if __name__ == '__main__':
	main()
