# interacting w mongoDB
test_trade = TestTrade()

test_trade.stock_ticker = 'SPOT'
test_trade.time_executed = timezone.now()
test_trade.trade_type = 'buy'
test_trade.num_shares = 2
test_trade.trade_amount = 20.20

# test_trade.save()

t = TestTrade.objects.get(pk=1)
