import django
import torch
import torch.nn as torch_nn

from services import test_suite
from tradeModels import MLModel as model
# from tradeModels import StockDataset as dataset

django.setup()
from tradeEngine.models import TestTrade

EPOCHS = 200

loss_function = model.loss_function

def main():
  test_suite.generate()
  test_suite.validate()
  # t = TestTrade.objects.get(pk=1)
  # print('t', t)
  input_dimension = 7
  output_dimension = 4
  # should hidden size be the same as the input dimension?
  hidden_dimension = 10
  batch_size = 20
  # do we really need mulitple layers?
  layers = 2
  # StockMLModel = model()
  # optimizer = model.optimizer
  lstm = torch_nn.LSTM(input_dimension, hidden_dimension)
  # seq_len, batch, input_size
  _input = torch.randn(batch_size, 1, input_dimension)
  # print('input', _input.size())

  out, (h, c) = lstm(_input)
  print(out.size())
  print(h.size())
  print(c.size())
  # for _ in range(EPOCHS):
  #   pass
  # train that bad boy





if __name__ == '__main__':
  main()
