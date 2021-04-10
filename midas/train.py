import django
import torch
import torch.nn as torch_nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from services import test_suite
from tradeModels.ml import StockDataset
from tradeModels.ml import StockLSTM as model

django.setup()
from tradeEngine.models import TestTrade

LEARNING_RATE = 0.05
EPOCHS = 200

def main():
  test_suite.generate()
  test_suite.validate()
  # t = TestTrade.objects.get(pk=1)
  # print('t', t)
  input_dimension = 7
  output_dimension = 4
  # should hidden size be the same as the input dimension?
  hidden_dimension = 100
  batch_size = 20
  # do we really need mulitple layers?
  layers = 2
  StockMLModel = model(
    input_dimension,
    hidden_dimension,
    output_dimension,
    layers
  )


  stocks = StockDataset(csv_file='data/model_data.csv')

  dataloader = DataLoader(
    stocks,
    batch_size=4,
    shuffle=True,
    num_workers=0,
    drop_last=True
  )

  loss_function = torch_nn.MSELoss()
  optimizer = optim.Adam(StockMLModel.parameters(), lr=LEARNING_RATE)

  losses = []
  for e in range(EPOCHS):
    batch_loss = 0
    for i, batch in enumerate(dataloader):
      out = StockMLModel(batch['data'].float())
      loss = loss_function(out, batch['label'].float())
      batch_loss += loss

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

      print(f'epoch: {e}, loss: {loss}')


if __name__ == '__main__':
  main()
