from django.http import HttpResponse
from django.utils import timezone

from tradeEngine.models import TestTrade

def HomeView(request):
  print('the home')
  t = TestTrade.objects.get(pk=1)
  print(t.stock_ticker)
  return HttpResponse('this is the midas home')