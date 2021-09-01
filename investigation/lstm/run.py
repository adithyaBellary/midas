import numpy as np
import torch
import torch.nn as torch_nn
import torch.nn.functional as F
import torch.optim as optim

NUM_FEATURES = 7
NUM_HIDDEN_FEATURES = 10
NUM_LAYERS = 2
NUM_PREDICTIONS = 3
NUM_ITEMS = 5

inputs = [torch.randn(NUM_ITEMS, NUM_FEATURES).view(NUM_ITEMS,1,NUM_FEATURES) for _ in range(5)]

class WordLSTM(torch_nn.Module):
  def __init__(self):
    super(WordLSTM, self).__init__()
    self.lstm = torch_nn.LSTM(
      NUM_FEATURES,
      NUM_HIDDEN_FEATURES,
      NUM_LAYERS,
      dropout=0.2,
      # if we want an output with dimensionality different than h
      proj_size=NUM_PREDICTIONS
    )

  def forward(self, x):
    # print('x', x.size())
    out, h = self.lstm(x)

    print('out in forward', out.size())
    print('h in forward', len(h))

    # we want an output of dimension [1, NUM_PREDICTIONS]
    out = torch.transpose(out.view(out.size()[0], out.size()[2]), 0, 1)

    linear_transform = torch_nn.Linear(NUM_ITEMS, 1)
    out = linear_transform(out)
    print('out in forward', out.size())
    return torch.transpose(out, 0, 1)

def main():
  model = WordLSTM()
  # print('first input', inputs[0])
  print('first input size', inputs[0].size())
  out = model(inputs[0])
  print('out in main', out.size())

if __name__ == '__main__':
  main()