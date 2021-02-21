from typing import Any, NamedTuple

class BarTick(NamedTuple):
  ticker: str
  o: float

  def __repr__(self):
    return f'ticker: {self.ticker} open {self.o}'