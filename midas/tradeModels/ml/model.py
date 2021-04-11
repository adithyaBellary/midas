import numpy as np
import torch
import torch.nn as torch_nn
import torch.nn.functional as F
import torch.optim as optim

# date of week, hour  open, close, high, low, volume
# let us encode day of week to be 1-5 (number)
INPUT_DIM = 7
# what are we predicting?
# open, high, low, close
# date and volume will just be inputs to these predictions
OUTPUT_DIM = 4
# based on this many number of minutes, we will make a prediction
INPUT_DATA_CHUNK_SIZE = 20

class StockLSTM(torch_nn.Module):
  def __init__(self, input_dimension, hidden_dimension, output_dimension, num_layers = 0 ):
    super(StockLSTM, self).__init__()
    self.input_dimension = input_dimension
    self.output_dimension = output_dimension
    self.hidden_dimension = hidden_dimension
    self.num_layers = num_layers

    self.gru = torch_nn.LSTM(
      self.input_dimension,
      self.hidden_dimension,
      self.num_layers,
      dropout=0.2
    )

    self.hidden_to_output = torch_nn.Linear(self.hidden_dimension, self.output_dimension)

  def forward(self, x):
    out, _ = self.gru(x)
    out = self.hidden_to_output(out[:, -1, :])

    # use  F.log_softmax(tag_space, dim=1) to convert scores -> probability (normalized to 1)
    return out


loss_function = torch_nn.MSELoss()
