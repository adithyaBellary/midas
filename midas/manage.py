#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv, find_dotenv

# from services.alpaca_trade_api import my_alpaca
# from services.alpaca_trade_api import my_alpaca
import services.alpaca_trade_api as my_alpaca

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midas.settings')
    # load env vars
    load_dotenv(find_dotenv())

    key_id = ''
    secret_key = ''
    base_url = ''

    if os.environ.get('DEBUG') == 'TRUE':
        key_id = os.environ.get('PAPER_KEY_ID')
        secret_key = os.environ.get('PAPER_SECRET_KEY')
        base_url = os.environ.get('PAPER_URL')
    else:
        key_id = os.environ.get('KEY_ID')
        secret_key = os.environ.get('SECRET_KEY')
        base_url = os.environ.get('URL')

    api = my_alpaca.REST(
        key_id=key_id,
        secret_key=secret_key,
        base_url=base_url
    )

    account = api.get_account()
    buying_power = account.buying_power
    print('buying power', buying_power)
    barData = api.get_barset('AAPL', 'day', limit=5)
    # print('bar data', barData.df)
    conn = my_alpaca.stream2.StreamConn(key_id=key_id, secret_key=secret_key)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
