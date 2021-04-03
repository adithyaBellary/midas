from torch.utils.data import Dataset, DataLoader
import pandas as pd

CHUNK_SIZE = 19

class StockDataset(Dataset):
  def __init__(self, csv_file: str):
    self.data = pd.read_csv(csv_file)

  def __len__(self):
    # return len(self.data)
    return int(len(self.data) / (CHUNK_SIZE + 1))

  def __getitem__(self, idx):
    # need to return the labels as well
    print(type(self.data.iloc[0].high))
    data = self.data.iloc[idx * CHUNK_SIZE : (idx + 1) * CHUNK_SIZE].to_numpy()
    print(f'{(idx + 1) * CHUNK_SIZE}')
    label = [
      self.data.iloc[(idx + 1) * CHUNK_SIZE].open,
      self.data.iloc[(idx + 1) * CHUNK_SIZE].close,
      self.data.iloc[(idx + 1) * CHUNK_SIZE].high,
      self.data.iloc[(idx + 1) * CHUNK_SIZE].low,
    ]
    return {
      'data': data,
      'label': label
    }
    # return self.data.iloc[idx]