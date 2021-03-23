import pandas as pd
from datetime import datetime, timedelta, date, time
import time as pytime
from typing import List
import logging
from pytz import timezone
import django
import os
from dotenv import load_dotenv, find_dotenv

from .typedefs import BarTick

logger = logging.getLogger()
ESTtz = timezone('EST')

load_dotenv(find_dotenv())
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midas.settings')
# need the django setup before we can access the models
django.setup()

from tradeEngine.models import TestTrade

class ScalpModel(object):
	def __init__(
		self,
		symbol: str,
		api,
		lot,
		testing: bool = False,
	):
		self.test_string: str = 'hello i am in the scalping algo!!!'
		# alpaca api so that we can submit trades and such
		self._lot = lot
		self._api = api
		self._bars = []
		# each class instance will take care of only one symbol
		self._symbol = symbol
		self._logger = logger.getChild(self._symbol)

		self.initialize_state()

		# check if the market is open
		clock = self._api.get_clock()
		# print('open', clock.next_open)
		# print('close', clock.next_close)
		now = self._now().strftime('%Y-%m-%d %H:%M')
		market_open = datetime.fromisoformat(now).replace(hour=9, minute=30)
		today = self._now(format=True)
		tomorrow = (self._now() + timedelta(days=1)).strftime('%Y-%m-%d')
		# print('now', now)
		# print('market_open', market_open)
		# print('tomorrow', tomorrow)

		# what if data gives us an empty data frame? like when starting this on the weekend or after market close
		# data = api.polygon.historic_agg_v2(self._symbol, 1, 'minute', today, tomorrow, unadjusted=False).df
		_from = datetime.fromisoformat('2020-12-22').strftime('%Y-%m-%d')
		to = datetime.fromisoformat('2020-12-23').strftime('%Y-%m-%d')
		# data = api.polygon.historic_agg_v2(
		#   'AAPL',
		#   1,
		#   'minute',
		#   _from,
		#   to,
		#   unadjusted=False).df

		# still have to figure out how to do this correctly
		# bars = data[market_open:]
		# self._bars = bars
		# print('data', data)
		# print('market_open', market_open)
		# print('data (sliced', data[market_open:])

		# close at 3:50
		self._closing_time = time(15, 50)
		# t = TestTrade.objects.get(pk=1)
		# print('t', t)

	def initialize_state(self):
		symbol = self._symbol
		order = [o for o in self._api.list_orders() if o.symbol == symbol]
		position = [p for p in self._api.list_positions() if p.symbol == symbol]
		self._order = order[0] if len(order) > 0 else None
		self._position = position[0] if len(position) > 0 else None

		if self._position is not None:
			if self._order is None:
				self._state = 'TO_SELL'
			else:
				self._state = 'SELL_SUBMITTED'
				if self._order.side != 'sell':
					self._logger.warn(f'state {self._state} mismatch order {self._order}')
		else:
			if self._order is None:
				self._state = 'TO_BUY'
			else:
				self._state = 'BUY_SUBMITTED'
				if self._order.side != 'buy':
					self._logger.warn(f'state {self._state} mismatch order {self._order}')

	def _outOfMarket(self) -> bool:
		return self._now().time() > self._closing_time

	def _now(self, format: bool = False):
		# we want to look at the time in EST
		now = datetime.now(tz=ESTtz)
		return now if not format else now.strftime('%Y-%m-%d')

	def update_time(self):
		api = self._api
		# account = api.get_account()
		today = self._now(format=True)
		cal = api.get_calendar(start=today, end=today)
		# print('cal', cal[0].open)
		clock = api.get_clock()
		# print('next open', clock.timestamp)
		myDate = date(clock.timestamp)
		print('my date', myDate)

	def checkup(self, position):
		# the housecleaning function that runs
		now = self._now()
		order = self._order
		# gets the timestamp
		# submitted_at example
		# this is all stored in utc time
		# 2020-12-29 01:18:44.506556+00:00
		# need to convert to est from utc (bc that what we are looking at by default)
		# order_submitted_at = datetime.fromisoformat(order.submitted_at).astimezone(ESTtz)
		print('ckecking up')
		if (
			order is not None and
			order.side == 'buy' and
			# make sure that it has been at least 2 mins since this order was submitted
			now - order_submitted_at > timedelta(minutes=2)
		):
			last_price = self._api.polygon.last_trade(self._symbol).price
			self._logger.info(f'cancelling missed buy order {order.id} as {order.limit_price} (current price is {last_price})')
			self._cancel_order()

		if self._position is not None and self._outOfMarket():
			print('selling in the checkup', self._symbol)
			print('the position:', self._position._raw)
			print('state', self._state)
			self._submit_sell(bailout=True)

	def _cancel_order(self):
		if self._order is not None:
			self._api.cancel_order(self._order.id)

	def _calc_buy_signal(self) -> bool:
		moving_avg = self._bars.rolling(20).mean().close.values
		closes = self._bars.close.values

		if closes[-2] < moving_avg[-2] and closes[-1] > moving_avg[-1]:
			self._logger.info(f'buy signal: closes[-2] {closes[-2]} < moving_avg {moving_avg[-2]} closes[-1] {closes[-1]} > moving_avg[-1] {moving_avg[-1]}')
			return True
		else:
			self._logger.info(f'closes[-2:] = {closes[-2:]}, mavg[-2:] = {mavg[-2:]}')
			return False

	def on_bar(self, bar):
		# so this function will get called on the streaming triggers
		# we will handle our state in here and submit trades based on that
		self._bars = self._bars.append(pd.DateFrame({
			'open': bar.open,
			'high': bar.high,
			'low': bar.low,
			'close': bar.close,
			'volume': bar.volume,
		}, index=[bar.start]))

		bar_len = len(self._bars)

		self._logger.info(f'received bar. start = {bar.start}, close = {bar.close}, len = {bar_len}')
		if bar_len < 21:
			return
		if self._outOfMarket():
			return
		if self._state == 'TO_BUY':
			if self._calc_buy_signal():
				self._submit_buy()

	def on_order_update(self, event, order):
		self._logger.info(f'order update: {event} = {order}')
		if event == 'fill':
			# clear the order
			self._order = None
			if self._state == 'BUY_SUBMITTED':
				self._position = self._api.get_position(self._symbol)
				self._transition('TO_SELL')
				self._submit_sell()
			elif self._state == 'SELL_SUBMITTED':
				self._position = None
				self._transition('TO_BUY')

				return
		elif event == 'partial_fill':
			self._position = self._api.get_position(self._symbol)
			self._order = self._api.get_order(order['id'])

			return
		elif event in ('canceled', 'rejected'):
			if event == 'rejected':
				self._logger.warn(f'order rejected: current order = {self._order}')
			self._order = None
			if self._state == 'BUY_SUBMITTED':
				if self._position is not None:
					self._transition('TO_SELL')
					self._submit_sell()
				else:
					self._transition('TO_BUY')
			elif self._state == 'SELL_SUBMITTED':
				self._transition('TO_SELL')
				self._submit_sell(bailout=True)
			else:
				self._logger.warn(f'unexpected state for {event}: {self._state}')

	def _submit_buy(self):
		trade = self._api.polygon.last_trade(self._symbol)
		amount = int(self._lot / trade.price)

		try:
			order = self._api.submit_order(
				symbol=self._symbol,
				side='buy',
				type='limit',
				qty=amount,
				time_in_force='day',
				limit_price=trade.price
			)
		except Exception as e:
			self._logger.warn(e)
			self._transition('TO_BUY')

			return

		self._order = order
		self._logger.info(f'submitted buy {order}')
		self._transition('BUY_SUBMITTED')

	def _submit_sell(self, bailout = False):
		# trade = self._api.polygon.last_trade(self._symbol)
		# amount = int(self._lot / trade.price)

		params = dict(
			symbol=self._symbol,
			side='sell',
			qty=self._position.qty,
			time_in_force='day'
		)

		if bailout:
			params['type'] = 'market'
		else:
			current_price = float(self._api.polygon.last_trade(self._symbol).price)
			cost_basis = float(self._position.avg_entry_price)
			limit_price = max(cost_basis + 0.01, current_price)

			params.update(dict(
				type='limit',
				limit_price=limit_price,
			))

		try:
			order = self._api.submit_order(**params)
		except Exception as e:
			self._logger.warn(e)
			self._transition('TO_SELL')

			return

		self._order = order
		self._logger.info(f'submitted sell {order}')
		self._transition('SELL_SUBMITTED')


	def _transition(self, new_state):
		self._logger.info(f'transition from {self._state} to {new_state}')
		self._state = new_state


	def get_olders(self):
		orders = [o for o in self._api.list_orders()]
		print(orders[0].submitted_at)
