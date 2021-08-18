# this engine is going to consume the lstm model and then make decisioning choices based on the bar data
import numpy as np
import torch

# different states of our engine
BOUGHT = 'bought'
TO_BUY = 'to buy'

class MlEngine:
  def __init__(self, weight_path: str, alpaca_api, input_length: int, lookahead: int):
    self.weight_path = weight_path
    self.lstm_model = self.load_model()
    self.api = alpaca_api
    self.INPUT_LENGTH = input_length
    self.input = []
    # how far away does this model predict?
    self.lookahead = lookahead
    self.state = TO_BUY

  def load_model(self):
    # load the weights into the model and then instantiate the lstm model
    return torch.load(self.weight_path)

  def clear_input(self):
    self.input = []

  def make_prediction(self):
    prediction = self.lstm_model(self.input)
    # submit order if it triggers the buy signal


  def on_bar(self, bar):
    self.input.append(bar)
    if len(self.input) == self.INPUT_LENGTH:
      self.make_prediction()
