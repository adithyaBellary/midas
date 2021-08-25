# this engine is going to consume the lstm model and then make decisioning choices based on the bar data
import numpy as np
import torch

# different states of our engine
BOUGHT = 'bought'
TO_BUY = 'to buy'
TO_SELL = 'to sell'

class MlEngine:
  def __init__(self, weight_path: str, alpaca_api, input_length: int, lookahead: int, stock: str):
    self.weight_path = weight_path
    self.lstm_model = self.load_model()
    self.api = alpaca_api
    self.INPUT_LENGTH = input_length
    self.input = []
    # how far away does this model predict?
    self.lookahead = lookahead
    self.state = TO_BUY
    self.buy_threshold = 1
    self.stock = stock

  def set_action_state(self, new_state):
    self.sate = new_state

  def submit_order(self, action):
    if action == TO_BUY:
      self.submit_buy_order()
      self.set_action_state(BOUGHT)

    if action == TO_SELL:
      self.submit_sell_order()
      self.set_action_state(TO_BUY)

  def submit_buy_order(self):
    # buy the stock
    pass

  def submit_sell_order(self):
    # sell the stock
    pass

  def load_model(self):
    # load the weights into the model and then instantiate the lstm model
    return torch.load(self.weight_path)

  def clear_input(self):
    self.input = []

  def calc_buy_trigger(self, prediction):
    if prediction >= self.buy_threshold & self.state == TO_BUY:
      return True

    return False

  def make_prediction(self):
    prediction = self.lstm_model(self.input)
    # submit order if it triggers the buy signal
    buy = self.calc_buy_trigger(prediction)
    # if it is going up

    # if it is going down

  def on_bar(self, bar):
    self.input.append(bar)
    if len(self.input) == self.INPUT_LENGTH:
      self.make_prediction()


      self.clear_input()
