import os
import services.alpaca_trade_api as tradeapi

key_id = ''
secret_key = ''
base_url = ''

if os.environ.get('DEBUG') == 'TRUE':
  key_id = os.environ.get('PAPER_KEY_ID')
  secret_key = os.environ.get('PAPER_SECRET_KEY')
  base_url = os.environ.get('PAPER_URL')
else:
  key_id = os.environ.get('KEY_ID')
  secret_key = os.environ.get('ALPACA_SECRET_KEY')
  base_url = os.environ.get('URL')

def setup_alpaca():
  # initialize clients

  api = tradeapi.REST(
    key_id=key_id,
    secret_key=secret_key,
    base_url=base_url
  )
  stream = my_alpaca.stream2.StreamConn(
    key_id=key_id,
    secret_key=secret_key,
    data_stream='polygon'
  )

  # add event triggers
  @stream.on(r'^Q')
  async def on_quote(conn, channel, data):
    print('in on_quote ', data)

  @conn.on(r'trade_updates')
  async def on_trade_update(conn, channel, data):
    print('there has been an update on our trade')

  @conn.on(r'trade_news')
  async def on_trade_news(conn, channel, data):
    # for future could somehow stream important news
    # related to stocks and such
    print('in on trade_news')

