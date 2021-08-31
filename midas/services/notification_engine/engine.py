from twilio.rest import Client

from django.conf import settings

class Notification:
  def __init__(self):
    self.TWILIO_SID = settings.TWILIO_SID
    self.TWILIO_AUTH = settings.TWILIO_AUTH
    self.TWILIO_NUMBER = settings.TWILIO_NUMBER
    self.MY_NUMBER = settings.MY_NUMBER

    self.client = Client(
      settings.TWILIO_SID,
      settings.TWILIO_AUTH
    )

  def send_message(self, message):
    self.client.messages.create(
      to=self.MY_NUMBER,
      from_=self.TWILIO_NUMBER,
      body=message
    )
