import django

from services import test_suite
from tradeModels import MLModel as model

django.setup()
from tradeEngine.models import TestTrade

def main():
  test_suite.generate()
  test_suite.validate()
  # t = TestTrade.objects.get(pk=1)
  # print('t', t)

if __name__ == '__main__':
  main()
