from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from twilio.twiml.messaging_response import MessagingResponse

from tradeEngine.models import TestTrade

@require_http_methods(["GET"])
def HomeView(request):
  print('the home')
  t = TestTrade.objects.get(pk=1)
  print(t.stock_ticker)
  return HttpResponse('this is the midas home')

# maybe we dont have to do exempy csrf for all post requests?
@csrf_exempt
@require_http_methods(["POST"])
def SMS(request):
  print('request method', request.method)
  resp = MessagingResponse()
  resp.message("The Robots are coming! Head for the hills!")

  return str(resp)
  # return HttpResponse('sms here')