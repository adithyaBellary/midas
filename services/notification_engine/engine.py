from twilio.rest import Client

from django.conf import settings

class Notification:
  def __init__(self):
    self.TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
    self.TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    self.TWILIO_NUMBER = settings.TWILIO_NUMBER
    self.MY_NUMBER = settings.MY_NUMBER

    self.client = Client(
      settings.TWILIO_ACCOUNT_SID,
      settings.TWILIO_AUTH_TOKEN
    )

  def send_message(self, message):
    self.client.messages.create(
      to=self.MY_NUMBER,
      from_=self.TWILIO_NUMBER,
      body=message
    )
