from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np

# CHUNK_SIZE = 19
# LOOKAHEAD = 1

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