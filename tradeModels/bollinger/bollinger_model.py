import numpy as np

BUY = 'buy'
SELL = 'sell'

class BollingerModel():
  def __init__(self, window, time_step, bollinger_band_1_multiplier, bollinger_band_2_multiplier, alpaca_api):
    self.window = window
    self.time_step = time_step

    self.moving_average = 0
    self.bollinger_1_upper = 0
    self.bollinger_1_lower = 0
    self.bollinger_2_upper = 0
    self.bollinger_2_lower = 0
    # how many std above / below ma do we want the bands to be?
    self.bollinger_band_1_multiplier = bollinger_band_1_multiplier
    self.bollinger_band_2_multiplier = bollinger_band_2_multiplier

    # this will be a list of dataframse
    self._bars = []
    self._bars_subset = []
    self._bar_threshold = 0.75

    self.alpaca_api = alpaca_api

    self.position = BUY

  def on_bar(self, bar):
    self._bar_current = bar
    self._bars.append(bar)
    # calculate moving average only if we have enough to start making bollinger bands

    if (len(self._bars) < self.window):
      return

    self.subset = self._bars[-1 * self.window:]
    ma = self.calc_moving_avg()
    std = self.calc_std_dev()

    # print('moving average', ma)
    # print('std', std)
    # make the bands
    self.bollinger_1_upper = ma + std * self.bollinger_band_1_multiplier
    self.bollinger_1_lower = ma - std * self.bollinger_band_1_multiplier

    self.bollinger_2_upper = ma + std * self.bollinger_band_2_multiplier
    self.bollinger_2_lower = ma - std * self.bollinger_band_2_multiplier

    # check the trigger
    b = self.check_buy_trigger()
    s = self.check_sell_trigger()

    if b:
      # make the trade
      # log it
      print('buying')

    if s:
      # made the trade
      # log it
      # pass
      print('selling')

  def is_bar_green(self) -> bool:
    return self._bar_current['open'] > self._bar_current['close']

  def check_bar_threshold(self, side: str) -> bool:
    # need to tune this

    is_green = self.is_bar_green()
    close = self._bar_current['close']
    o = self._bar_current['open']
    candle_stick_height = abs(o - close)
    # print('is green', is_green)
    # print('time:', self._bar_current['timestamp'])
    # print('close:', self._bar_current['close'])
    # print('band lower:', self.bollinger_lower)
    # print('band upper:', self.bollinger_upper)
    if side == BUY:
      return is_green & (self._bar_threshold * candle_stick_height) (self.bollinger_1_lower)
    if side == SELL:
      return (not is_green) & (close * (1 - self._bar_threshold) <= self.bollinger_1_upper)

  def check_buy_trigger(self):

    return self.check_bar_threshold(BUY)

  def check_sell_trigger(self):

    return self.check_bar_threshold(SELL)

  def get_relevant_fields(self, frame):
    # average the columns that we want
    # could just be the open price or a combination of open, high, low, close

    return np.average([frame['high'], frame['low'], frame['close']])

  def calc_moving_avg(self):
    # slice _bars

    # should we calculate the moving average across the open prices?
    # the average of the high, low, and close proces?
    bar_sum = sum([self.get_relevant_fields(i) for i in self.subset])
    # print('bar sum', bar_sum)
    avg = bar_sum / self.window
    # print('avg', avg)
    return avg

  def calc_std_dev(self):
    std = np.std([self.get_relevant_fields(i) for i in self.subset])
    return std

