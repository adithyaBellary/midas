from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np

CHUNK_SIZE = 19
LOOKAHEAD = 1

class StockDataset(Dataset):
  def __init__(self, csv_file: str):
    self.data = pd.read_csv(csv_file)

  def __len__(self):
    # return len(self.data)
    return len(self.data) - (CHUNK_SIZE + LOOKAHEAD)

  def __getitem__(self, idx):
    # need to return the labels as well
    # data = self.data.iloc[idx * CHUNK_SIZE : (idx + 1) * CHUNK_SIZE].to_numpy().astype(np.double)
    data = self.data.iloc[idx : idx + CHUNK_SIZE].to_numpy().astype(np.double)
    label = np.array([
      self.data.iloc[idx + CHUNK_SIZE].open,
      self.data.iloc[idx + CHUNK_SIZE].close,
      self.data.iloc[idx + CHUNK_SIZE].high,
      self.data.iloc[idx + CHUNK_SIZE].low,
      ],
      dtype=np.double
    )
    return {
      'data': data,
      'label': label
    }