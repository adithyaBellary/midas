import numpy as np
import torch
import torch.nn as torch_nn
import torch.nn.functional as F
import torch.optim as optim

NUM_FEATURES = 7
NUM_HIDDEN_FEATURES = 10
NUM_LAYERS = 2
NUM_PREDICTIONS = 3

inputs = [torch.randn(2, 3).view(2,3,1) for _ in range(5)]

class WordLSTM(torch_nn.Module):
  def __init__(self):
    super(WordLSTM, self).__init__()
    self.lstm = torch_nn.LSTM(
      NUM_FEATURES,
      NUM_HIDDEN_FEATURES,
      NUM_LAYERS,
      dropout=0.2,
      # proj_size=NUM_PREDICTIONS
    )

  def forward(self, x):
    print('x', x.size())
    out, h = self.lstm(x)

    print(out)
    print(h)

    return out

def main():
  model = WordLSTM()
  print('first input', inputs[0])
  print('first input size', inputs[0].size())
  out = model(inputs[0])
  print('hi')
  print('out', out)

if __name__ == '__main__':
  main()