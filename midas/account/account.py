class Acount():
  def __init__(self, alpaca_api):
    self.profit = 0
    self._api = alpaca_api
    self.buying_power = 0
    self.exposure = 0