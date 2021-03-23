import pandas as pd
import numpy as np
import time
import logging
import asyncio
import threading
from dotenv import load_dotenv, find_dotenv
import sys
import os

from services import alpaca_trade_api as tradeapi
# import tradeModels.scalping as scalpModel
from tradeModels import ScalpModel as scalpModel
import tradeEngine

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
	buying_power = account.buying_power
	# print(api.list_orders())
	# print('buying power', buying_power)
	# t = TestTrade.objects.get(pk=1)
	# print('t', t)
	# print(polygon.last_quote('AAPL'))

	# getting a 401 (unauthorized error on this for some reason)
	# data = polygon.historic_agg_v2(
	# 	'AAPL',
	# 	1,
	# 	'minute',
	# 	'2021-02-01',
	# 	'2021-02-02',
	# 	# unadjusted=False,
	# 	# limit=5000
	# 	).df
	# data.to_csv('test.csv')
	# print('test data', data.head())
	# hardcoding the stocks of interesst might not be the best way forward
	symbols = ['NIO', 'AAPL', 'MSFT']
	scalp_algos = {}
	lot = 10

	for sym in symbols:
		scalp_algos[sym] = scalpModel.ScalpModel(sym, api, lot)

	@conn.on(r'^AM')
	async def on_AM(conn, channel, data):
		print('in AM ', data.symbol)
		if data.symbol in scalp_algos:
			scalp_algos[data.symbol].on_bar(data)

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
		# print('in on_trade_updates ', data)
		logger.info(f'trade_updates {data}')
		symbol = data.order['symbol']
		if symbol in scalp_algos:
			scalp_algos[symbol].on_order_update(data.event, data.order)

	@conn.on(r'^status')
	async def on_status(conn, channel, data):
		# print('channel: {}, data: {}'.format(channel, data))
		print('channel')
		# pass

	async def scalp_periodic():
		while True:
			if not api.get_clock().is_open:
				# here is where we should sleep until the next market open
				print('we not open, waiting 1')
				await asyncio.sleep(10)
				# logger.info('exit as market is not open')
				# sys.exit(0)

			# print('checking up')
			await asyncio.sleep(15)
			positions = api.list_positions()
			# print('positions', [p._raw for p in positions])
			for symbol, algo in scalp_algos.items():
				pos = [p for p in positions if p.symbol == symbol]
				algo.checkup(pos[0] if len(pos) > 0 else None)

	channels = ['trade_updates'] + ['AM.' + symbol for symbol in symbols]

	# conn.run(channels)
	# need to rethink how this runs
	loop = conn.loop
	loop.run_until_complete(asyncio.gather(
		# need to make sure that just subscribing to the channels actually consumes the messages from the ws
		conn.subscribe(channels),
		scalp_periodic(),
	))
	loop.close()

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
