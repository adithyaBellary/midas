from services.notification_engine import Notification

def main():
  notif_engine = Notification()
  notif_engine.send_message(message='testing 123')
# https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
if __name__ == '__main__':
  main()