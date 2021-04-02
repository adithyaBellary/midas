from torch.utils.data import Dataset, DataLoader
import pandas as pd

class StockDataset(Dataset):
  def __init__(self, csv_file: str):
    self.data = pd.read_csv(csv_file)

  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    # need to return the labels as well
    return self.data.iloc[idx]