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
load_dotenv(find_dotenv())

KEY_ID = os.environ.get('KEY_ID')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
URL = os.environ.get('URL')

PAPER_KEY_ID = os.environ.get('PAPER_KEY_ID')
PAPER_SECRET_KEY = os.environ.get('PAPER_SECRET_KEY')
PAPER_URL = os.environ.get('PAPER_URL')

class Quote():
    """
    We use Quote objects to represent the bid/ask spread. When we encounter a
    'level change', a move of exactly 1 penny, we may attempt to make one
    trade. Whether or not the trade is successfully filled, we do not submit
    another trade until we see another level change.

    Note: Only moves of 1 penny are considered eligible because larger moves
    could potentially indicate some newsworthy event for the stock, which this
    algorithm is not tuned to trade.
    """

    def __init__(self, use_threading = False):
        self.prev_bid = 0
        self.prev_ask = 0
        self.prev_spread = 0
        self.bid = 0
        self.ask = 0
        self.bid_size = 0
        self.ask_size = 0
        self.spread = 0
        self.traded = True
        self.level_ct = 1
        self.time = 0
        self._use_threading = use_threading

        # TODO:
        # add rlocks when we decide to use threading
    def reset(self):
        # Called when a level change happens
        # add rlock
        self.traded = False
        self.level_ct += 1

    def update(self, data):
        # Update bid and ask sizes and timestamp
        # add rlock
        self.bid_size = data.bidsize
        self.ask_size = data.asksize

        # Check if there has been a level change
        if (
            self.bid != data.bidprice
            and self.ask != data.askprice
            and round(data.askprice - data.bidprice, 2) == .01
        ):
            # Update bids and asks and time of level change
            self.prev_bid = self.bid
            self.prev_ask = self.ask
            self.bid = data.bidprice
            self.ask = data.askprice
            self.time = data.timestamp
            # Update spreads
            self.prev_spread = round(self.prev_ask - self.prev_bid, 3)
            self.spread = round(self.ask - self.bid, 3)
            print(
                'Level change:', self.prev_bid, self.prev_ask,
                self.prev_spread, self.bid, self.ask, self.spread, flush=True
            )
            # If change is from one penny spread level to a different penny
            # spread level, then initialize for new level (reset stale vars)
            if self.prev_spread == 0.01:
                self.reset()

class Stocks():
    def __init__(self, stock_list = None):
        # this class is meant to keep track of stock movements for that day
        # keep track of the highs and lows?
        self._stocks = stock_list

    def reset(self):
        # clear the stocks list
        pass

class Batcher():
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.empty = True

class Position():
    """
    The position object is used to track how many shares we have. We need to
    keep track of this so our position size doesn't inflate beyond the level
    we're willing to trade with. Because orders may sometimes be partially
    filled, we need to keep track of how many shares are "pending" a buy or
    sell as well as how many have been filled into our account.
    """

    def __init__(self, use_threading = False):
        self.orders_filled_amount = {}
        self.pending_buy_shares = 0
        self.pending_sell_shares = 0
        self.total_shares = 0
        self._use_threading = use_threading

        # TODO:
        # attempt to see what thread we are a part of
        # then we can see whether a new object actually gets made each time

        # TODO
        # add rlocks when accessing data
        # to prevent accessing the same resource
        # when we decide to use the threading method that is

    def update_pending_buy_shares(self, quantity):
        self.pending_buy_shares += quantity

    def update_pending_sell_shares(self, quantity):
        self.pending_sell_shares += quantity

    def update_filled_amount(self, order_id, new_amount, side):
        old_amount = self.orders_filled_amount[order_id]
        if new_amount > old_amount:
            if side == 'buy':
                self.update_pending_buy_shares(old_amount - new_amount)
                self.update_total_shares(new_amount - old_amount)
            else:
                self.update_pending_sell_shares(old_amount - new_amount)
                self.update_total_shares(old_amount - new_amount)
            self.orders_filled_amount[order_id] = new_amount

    def remove_pending_order(self, order_id, side):
        old_amount = self.orders_filled_amount[order_id]
        if side == 'buy':
            self.update_pending_buy_shares(old_amount - 100)
        else:
            self.update_pending_sell_shares(old_amount - 100)
        del self.orders_filled_amount[order_id]

    def update_total_shares(self, quantity):
        self.total_shares += quantity

#time -> time period
#stock -> stock ticker(s) of interest. a list
# poly -> polygon api

# looks like we cant get the second data :(
# throws an error when we set size = "minute"
def get_history(time, stock, poly):
    hist = {}
    for stock_symb in stock:
        hist[stock_symb] = poly.historic_agg_v2(
            size="minute",
            symbol=stock_symb,
            limit=time
        ).df
    return hist

def run():

    max_shares = 100
    _use_threading = False
    quote = Quote(use_threading=_use_threading)
    position = Position(use_threading=_use_threading)
    api = tradeapi.REST(key_id=PAPER_KEY_ID, secret_key=PAPER_SECRET_KEY, base_url=PAPER_URL)
    # my_api = my_trade_api.rest.REST(key_id=PAPER_KEY_ID, secret_key=PAPER_SECRET_KEY)
    poly = api.polygon

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    _logger = logging.getLogger(__name__)

    # Establish streaming connection
    api_key_id = PAPER_KEY_ID
    api_secret = PAPER_SECRET_KEY
    _stocks = ["AAPL"]
    # 50k seems to be the limit
    # test_data = get_history(time=50000, stock=_stocks, poly=poly)
    # for ind, row in test_data["AAPL"].iterrows():
    #     print(row)



    # if we want to use multithreading
    # conn = tradeapi.stream2.StreamConn(key_id=api_key_id, secret_key=api_secret, logger=_logger, use_threading=_use_threading, test_data=test_data)
    # if we do not want to use multithreading

    # this seems to be pointint to the installed package of alpaca tradeapi
    # we dont want that. would rather have it point to my local version
    conn = tradeapi.StreamConn(key_id=api_key_id, secret_key=api_secret, data_stream='polygon')


    # track our buying power
    account = api.get_account()
    buying_power = account.buying_power
    _logger.info('${} is how much buying power you have'.format(buying_power))

    # if we want to get the bar data:
    # this will get us the daily bar data for AAPL over the last 5 trading days
    barData = api.get_barset('AAPL', 'day', limit=5)

    # Define our message handling
    @conn.on(r'^Q')
    async def on_quote(conn, channel, data):
        # Quote update received
        # print('in on_quote ', data)
        quote.update(data)

    @conn.on(r'^AM')
    async def on_AM(conn, channel, data):
      print('in AM ', data)

    @conn.on(r'^A')
    async def on_A(conn, channel, data):
      print('in A ')

    @conn.on(r'^T')
    async def on_trade(conn, channel, data):
        print('in on_trade ')

        if quote.traded:
            print('quote was traded')
            return
        # We've received a trade and might be ready to follow it
        if (
            data.timestamp <= (
                quote.time + pd.Timedelta(np.timedelta64(50, 'ms'))
            )
        ):
            # The trade came too close to the quote update
            # and may have been for the previous level
            return
        if data.size >= 100:
            # The trade was large enough to follow, so we check to see if
            # we're ready to trade. We also check to see that the
            # bid vs ask quantities (order book imbalance) indicate
            # a movement in that direction. We also want to be sure that
            # we're not buying or selling more than we should.
            if (
                data.price == quote.ask
                and quote.bid_size > (quote.ask_size * 1.8)
                and (
                    position.total_shares + position.pending_buy_shares
                ) < max_shares - 100
            ):
                # Everything looks right, so we submit our buy at the ask
                try:
                    o = api.submit_order(
                        symbol=symbol, qty='100', side='buy',
                        type='limit', time_in_force='day',
                        limit_price=str(quote.ask),
                        extended_hours=True,
                    )
                    # Approximate an IOC order by immediately cancelling
                    api.cancel_order(o.id)
                    position.update_pending_buy_shares(100)
                    position.orders_filled_amount[o.id] = 0
                    print('Buy at', quote.ask, flush=True)
                    quote.traded = True
                except Exception as e:
                    print(e)
            elif (
                data.price == quote.bid
                and quote.ask_size > (quote.bid_size * 1.8)
                and (
                    position.total_shares - position.pending_sell_shares
                ) >= 100
            ):
                # Everything looks right, so we submit our sell at the bid
                try:
                    o = api.submit_order(
                        symbol=symbol, qty='100', side='sell',
                        type='limit', time_in_force='day',
                        limit_price=str(quote.bid),
                        extended_hours=True,
                    )
                    # Approximate an IOC order by immediately cancelling
                    api.cancel_order(o.id)
                    position.update_pending_sell_shares(100)
                    position.orders_filled_amount[o.id] = 0
                    print('Sell at', quote.bid, flush=True)
                    quote.traded = True
                except Exception as e:
                    print(e)

    @conn.on(r'trade_updates')
    async def on_trade_updates(conn, channel, data):
        # We got an update on one of the orders we submitted. We need to
        # update our position with the new information.
        print('in on_trade_updates ', data)
        # TODO
        # write to db here
        event = data.event
        if event == 'fill':
            if data.order['side'] == 'buy':
                position.update_total_shares(
                    int(data.order['filled_qty'])
                )
            else:
                position.update_total_shares(
                    -1 * int(data.order['filled_qty'])
                )
            position.remove_pending_order(
                data.order['id'], data.order['side']
            )
        elif event == 'partial_fill':
            position.update_filled_amount(
                data.order['id'], int(data.order['filled_qty']),
                data.order['side']
            )
        elif event == 'canceled' or event == 'rejected':
            position.remove_pending_order(
                data.order['id'], data.order['side']
            )

    # doubt these are actual channels
    @conn.on(r'trade_news')
    async def on_trade_news(conn, channel, data):
        # for future could somehow stream important news
        # related to stocks and such
        print('in on trade_news')

    @conn.on(r'gibberish')
    async def testing_stuff(conn, channel, data):
        print('in on gibbe')


    @conn.on(r'^status')
    async def on_status(conn, channel, data):
        _logger.info('channel: {}, data: {}'.format(channel, data))

    async def s(t):
        _logger.info('started sleeping in s()')
        await asyncio.sleep(t)
        _logger.info('done sleeping in s()')

    conn.run(
        ['T.AAPL', 'Q.AAPL', 'T.AMZN', 'A.AAPL', 'AM.AAPL']
    )

def run_hft():
  run()


if __name__ == '__main__':
  main()
