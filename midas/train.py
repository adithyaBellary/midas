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

LEARNING_RATE = 0.1
EPOCHS = 150

def main():
  test_suite.generate()
  test_suite.validate()
  # t = TestTrade.objects.get(pk=1)
  # print('t', t)
  input_dimension = 7
  output_dimension = 4
  # should hidden size be the same as the input dimension?
  hidden_dimension = 50
  batch_size = 20
  # do we really need mulitple layers?
  layers = 2
  StockMLModel = model(
    input_dimension,
    hidden_dimension,
    output_dimension,
    layers
  )
  # optimizer = model.optimizer
  # lets use GRU over LSTM
  lstm = torch_nn.GRU(input_dimension, hidden_dimension, 2)
  # seq_len, batch, input_size
  _input = torch.randn(batch_size, 1, input_dimension)
  linear = torch_nn.Linear(hidden_dimension, output_dimension)


  out, (h, c) = lstm(_input)

  t = torch.Tensor([[1,2,3], [4,5,6]])
  out_linear = linear(out[-1, :, :])

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
  # print('len of dataloader', len(dataloader))
  for e in range(EPOCHS):
    for i, batch in enumerate(dataloader):
      # print('i', i)
      # if (i == 0):
      #   print('batch', batch['data'].float())
      #   print('batch', batch['label'].shape)
      out = StockMLModel(batch['data'].float())
      # print('out size', out.size())
      # print('label size', batch['label'].size())

      loss = loss_function(out, batch['label'].float())
      losses.append(loss)
      loss.backward()
      optimizer.step()
      print(f'epoch: {e}, loss: {loss}')

    # step optimizer
    # print loss and error at this time





if __name__ == '__main__':
  main()
