from djongo import models
# from django.db import models

import datetime
from django.utils import timezone

# Create your models here.
# these models will be what is used with the db

# A Test Trade Object
class TestTrade(models.Model):
  # the stock that was traded
  stock_ticker = models.CharField(max_length=20)
  # when the trade was executed
  time_executed = models.DateTimeField('time traded')
  # buy or sell?
  trade_type = models.CharField(max_length=20)
  # number of shared traded
  num_shares = models.IntegerField(default=0)
  # trade amount
  trade_amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)

  def __str__(self):
    return f'{self.stock_ticker} was traded'