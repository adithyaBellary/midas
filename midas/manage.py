#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv, find_dotenv
import threading
import django

from test_hft import run_hft

load_dotenv(find_dotenv())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midas.settings')

def main():
  """Run administrative tasks."""

  try:
    from django.core.management import execute_from_command_line
  except ImportError as exc:
    raise ImportError(
      "Couldn't import Django. Are you sure it's installed and "
      "available on your PYTHONPATH environment variable? Did you "
      "forget to activate a virtual environment?"
    ) from exc

  if sys.argv[1] == 'runserver':
    # if we are starting the server, load up the alpaca engine also
    t = threading.Thread(target=run_hft, args=[])
    t.start()
    # run_hft()
  execute_from_command_line(sys.argv)


if __name__ == '__main__':
  main()
