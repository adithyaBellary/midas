from torch.utils.data import Dataset
import torch
import pandas as pd
import numpy as np

class StockDataset(Dataset):
  def __init__(self, csv_file: str, input_size: int, lookahead: int):
    self.data = pd.read_csv(csv_file)
    self.input_size = input_size
    self.lookahead = lookahead

  def __len__(self):
    return len(self.data) - (self.input_size + self.lookahead)

  def __getitem__(self, idx):
    data = self.data.iloc[idx : idx + self.input_size].to_numpy().astype(np.double)
    # is this what we really need to predict?
    # we dont necessarily need to predict the high and low
    label = np.array([
      self.data.iloc[idx + self.input_size].open,
      self.data.iloc[idx + self.input_size].close,
      self.data.iloc[idx + self.input_size].high,
      self.data.iloc[idx + self.input_size].low,
      ],
      dtype=np.double
    )
    return {
      'data': data,
      'label': label
    }

# we can try using %change because that is at the core at what we are trying to predict
# we care more about how the price is going to change then what it is exactly

# encode
# [%change of close, %change bid size, %change bid price, %change ask size, %change ask price]
# could also encode
# [%change of open, %change of close, %change of high, %change of low, %change of volume]

# not sure if i should bother with quote data. quote data rolls up into the open and close prices
# and that is really what we want in the end

# predict
# % change close
class SeqDataset(Dataset):
  def __init__(self, csv_file: str, input_size: int, lookahead: int):
    self.data = pd.read_csv(csv_file)
    self.csv_file = csv_file
    self.input_size = input_size
    self.lookahead = lookahead

  def sanitize_bars(self, reduce_factor: int):
    d = pd.read_csv(self.csv_file)
    # pare down the rows

  def __len__(self):
    return len(self.data) - self.input_size - self.lookahead

  # this will return a percent, not a decimal
  # there will not be much change from minute to minute, so the
  # very small numbers (e-4) might be hard the model to detect differences
  def get_precent_change(self, a: float, b: float) -> float:
    return ((b-a) / a) * 100

  def get_bar(self, prev_bar, current_bar):
    return [
      self.get_precent_change(prev_bar.open, current_bar.open),
      self.get_precent_change(prev_bar.close, current_bar.close),
      self.get_precent_change(prev_bar.high, current_bar.high),
      self.get_precent_change(prev_bar.low, current_bar.low),
      self.get_precent_change(prev_bar.volume, current_bar.volume),
    ]

  def __getitem__(self, idx):
    bars = self.data.iloc[idx : idx + 1 + self.input_size + self.lookahead]
    treated_bars = [self.get_bar(bars.iloc[i], bars.iloc[i+1]) for i in range(len(bars)-1)]
    # print('treated bars', treated_bars[0])
    # print('all treated bars', treated_bars)
    data = treated_bars[:self.input_size]
    label = treated_bars[-1][0]
    # print('treated bars', treated_bars)
    # print('data', data)
    # print('label', np.array(label).shape)
    # print('label', label)

    return {
      'data': data,
      'label': label
    }

