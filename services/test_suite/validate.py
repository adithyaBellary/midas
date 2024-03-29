import csv
from datetime import datetime, timedelta, date, time
import pandas as pd

HIGH = 'high'
LOW = 'low'
OPEN = 'open'
CLOSE = 'close'
VOLUME = 'volume'
DAY = 'day'
HOUR = 'hour'

DATA_LENGTH = 15
ALLOW_IMPERFECT = False
MODEL_DATA_FILENAME = 'data/model_data.csv'

def get_day_from_date(d: str) -> str:
  d_iso = datetime.fromisoformat(d)
  weekday = d_iso.isoweekday()
  return str(weekday)

def get_hour_from_date(d: str) -> str:
  d_iso = datetime.fromisoformat(d)
  hour = d_iso.hour

  return str(hour)

def treat_row(row: object) -> object:
  return {
    OPEN: float(row.open) / 100,
    CLOSE: float(row.close) / 100,
    HIGH: float(row.high) / 100,
    LOW: float(row.low) / 100,
    VOLUME: float(row.volume) / 1000000,
    DAY: get_day_from_date(row.timestamp),
    HOUR: get_hour_from_date(row.timestamp)
  }

def validate(file_name: str):
  csv_data = pd.read_csv(f'data/{file_name}.csv')
  # print('csv data', csv_data.iloc[0])
  # print(csv_data.iloc[0].high)
  # print(treat_row(csv_data.iloc[0]))
  treated_df = pd.DataFrame(
    [treat_row(csv_data.iloc[i]) for i in range(len(csv_data))],
    columns=[OPEN, CLOSE, HIGH, LOW, VOLUME, DAY, HOUR]
  )
  # print(treated_df.head())
  treated_df.to_csv(MODEL_DATA_FILENAME, index=False)
