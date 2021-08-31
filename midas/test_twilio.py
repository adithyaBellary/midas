from services.notification_engine import Notification

def main():
  # test wilio
  notif_engine = Notification()
  notif_engine.send_message(message='testing 123')

if __name__ == '__main__':
  main()