import numpy as np
import torch
import torch.nn as torch_nn
import torch.nn.functional as F
import torch.optim as optim

# date of week, hour  open, close, high, low, volume
# let us encode day of week to be 1-5 (number)
# INPUT_DIM = 7
# what are we predicting?
# open, high, low, close
# date and volume will just be inputs to these predictions
# OUTPUT_DIM = 4
# based on this many number of minutes, we will make a prediction
# INPUT_DATA_CHUNK_SIZE = 20

class StockLSTM(torch_nn.Module):
  # this model predicts just one time step ahead
  # i feel like we need more than that
  def __init__(self, input_dimension, hidden_dimension, output_dimension, prediction_timespan, num_layers ):
    super(StockLSTM, self).__init__()
    self.input_dimension = input_dimension
    self.output_dimension = output_dimension
    self.hidden_dimension = hidden_dimension
    self.num_layers = num_layers
    # how many timesteps will be fed in at one time
    self.prediction_timespan = prediction_timespan

    self.lstm = torch_nn.LSTM(
      self.input_dimension,
      self.hidden_dimension,
      self.num_layers,
      dropout=0.2,
      proj_size=output_dimension,
      # input and output tensors are going to be
      # (batch, seq, eature) intead of (sequence, batch, feature) now
      # batch_first=True
    )

    self.timespan_reduction = torch_nn.Linear(prediction_timespan, 1)

  def forward(self, x):
    # print('input size', x.size())
    out, _ = self.lstm(x)
    # output will be (batch, seq, feature), so (1, prediction_timespan, output_dimension)
    output_size = out.size()
    # print('output size', output_size)
    out = torch.transpose(out.view(output_size[0], output_size[2]), 0, 1)
    # print('output size after transpose', out.size())
    out = self.timespan_reduction(out)
    # print('output size after size reduction', out.size())
    out = torch.transpose(out, 0, 1)
    # print('out size at the very end', out.size())
    # print('out value', out)
    return out


loss_function = torch_nn.MSELoss()
