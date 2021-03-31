import csv
from datetime import datetime, timedelta, date, time

DATA_LENGTH = 15
ALLOW_IMPERFECT = False
MODEL_DATA_FILENAME = 'model_data.csv'

def get_day_from_date(d: str):
  d_iso = datetime.fromisoformat(d)

  return d_iso.isoweekday()

def get_time_from_date(d: str):
  d_iso = datetime.fromisoformat(d)
  hour = d_iso.hour

  return hour

def validate():
  d = []
  with open('test.csv', newline='') as csvFile:
    dataReader = csv.reader(csvFile, delimiter=',')
    for index, r in enumerate(dataReader):
      print('r', r)
      if index != 0:
        # we do not want to add the header row to the data array
        d.append(r)

  treated_data = []
  for row in d:
    a = []
    for index, val in enumerate(row):
      if index == 0:
        a.append(get_day_from_date(val))
        a.append(get_time_from_date(val))
      else:
        a.append(float(val))

    treated_data.append(a)

  with open(MODEL_DATA_FILENAME, 'w', newline='') as csvFile:
    data_writer = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in treated_data:
      data_writer.writerow(row)


