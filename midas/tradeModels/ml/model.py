import numpy as np
import torch
import torch.nn as torch_nn
import torch.nn.functional as F
import torch.optim as optim

# date of week, open, close, high, low, volume
# let us encode day of week to be 1-5 (number)
INPUT_DIM = 6
# what are we predicting?
# open, high, low, close
# date and volume will just be inputs to these predictions
OUTPUT_DIM = 4
# based on 15 minutes, we will make a prediction
INPUT_DATA_CHUNK_SIZE = 15

class StockLSTM(torch_nn.Module):
  def __init__(self, input_dimension, output_dimension, hidden_dimension):
    super(StockLSTM, self).__init__()
    self.input_dimension = input_dimension
    self.output_dimension = output_dimension
    self.hidden_dimension = hidden_dimension

    self.lstm = torch_nn.LSTM(self.input_dimension, self.hidden_dimension)

    self.hidden_to_output = torch_nn.Linear(self.hidden_dimension, self.output_dimension)

  def forward(self, x):
    print('x', x)
    out = self.lstm(x)
    print('out', out)
    output = self.hidden_to_output(out)
    print('output', output)

    # use  F.log_softmax(tag_space, dim=1) to convert scores -> probability (normalized to 1)

loss_function = torch_nn.MSELoss()

