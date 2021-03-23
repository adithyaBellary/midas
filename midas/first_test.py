from services import test_suite
from tradeEngine.models import TestTrade

def main():
  # test_suite.generate()
  t = TestTrade.objects.get(pk=1)
  print('t', t)

if __name__ == '__main__':
  main()
