import django
import torch
import torch.nn as torch_nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import numpy as np

from services import test_suite
from tradeModels.ml import StockDataset, SeqDataset
from tradeModels.ml import StockLSTM as model

django.setup()
from tradeEngine.models import TestTrade

# t = TestTrade.objects.get(pk=1)
# print('t', t)

LEARNING_RATE = 0.01
EPOCHS = 1
# EPOCHS = 0

STOCK = 'AAPL'
FILE = 'new_lstm'
MODEL_DATA_CSV = 'data/model_data.csv'
NUM_DAYS_TRAINING_DATA = 100

# need to move this to a config module
# how many input features we will be having
NUM_INPUT_FEATURES = 5
# how many features are we predicting (just the close price percentage)
NUM_OUTPUT_FEATURES = 1
# hidden layer dimension
HIDDEN_DIMENSION = 75
# how many timesteps is our input data chunk
INPUT_LENGTH = 25
# num lstm layers
NUM_LAYERS = 2
# how far ahead are we predicting
lookahead = 15

def main():
  test_suite.generate(
    STOCK,
    FILE,
    NUM_DAYS_TRAINING_DATA,
  )
  # test_suite.validate(FILE)

  StockMLModel = model(
    NUM_INPUT_FEATURES,
    HIDDEN_DIMENSION,
    NUM_OUTPUT_FEATURES,
    INPUT_LENGTH,
    NUM_LAYERS
  )

  # stocks = StockDataset(
  #   MODEL_DATA_CSV,
  #   INPUT_LENGTH,
  #   lookahead
  # )

  seqStocks = SeqDataset(
    'data/new_lstm.csv',
    INPUT_LENGTH,
    lookahead
  )

  dataloader = DataLoader(
    seqStocks,
    batch_size=1,
    shuffle=True,
    num_workers=1,
    drop_last=True
  )

  loss_function = torch_nn.MSELoss()
  optimizer = optim.Adam(StockMLModel.parameters(), lr=LEARNING_RATE)

  losses = []
  for e in range(EPOCHS):
    batch_loss = 0
    for i, batch in enumerate(dataloader):
      data = torch.Tensor(batch['data'])
      data_size = data.size()
      data_reshape = data.view(data_size[0],1,data_size[1])
      label = batch['label'].float()

      out = StockMLModel(data_reshape)
      loss = loss_function(out.view(1), label)

      batch_loss += loss

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

      if (i % 500 == 0):
        print(f'i: {i}, epoch: {e}, loss {loss}')


    print(f'epoch: {e}, loss: {batch_loss}')

    losses.append(batch_loss)

  plt.plot(losses)
  plt.ylabel('losses')
  plt.xlabel('epoch')
  ID = '300_days_40_epochs'
  FIGURE_NAME = f'figures/loss_{ID}.png'
  plt.savefig(FIGURE_NAME)
  # plt.show()

  # save the model
  PATH = f'weights/model_{ID}.pt'
  torch.save(StockMLModel, PATH)

if __name__ == '__main__':
  main()
