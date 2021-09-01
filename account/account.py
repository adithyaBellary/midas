class Account():
  def __init__(self, alpaca_api, mocked: bool):
    self._api = alpaca_api
    self.mocked = mocked

  def get_buying_power(self):
    acc = self._api.get_account()
    return acc.buying_power

  def process_trade(self, stock, price, positon):
    pass
