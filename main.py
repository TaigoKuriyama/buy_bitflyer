import os

import ccxt


def buy_btc(event, context):
    """ BTC  """
    bf = ccxt.bitflyer()
    bf.apiKey = os.environ.get("api_key", None)
    bf.secret = os.environ.get("api_secret", None)
    amt_buy = int(os.environ.get("amt_yen", None))

    i = 0
    is_not_done = True
    price_list = []
    size_list = []
    unfilled_yen = amt_buy
    orderbook = bf.fetch_order_book('BTC/JPY')

    while is_not_done:
        best_ask_price = float(orderbook['asks'][i][0])
        best_ask_size = float(orderbook['asks'][i][1])
        price_list.append(best_ask_price)
        size_list.append(best_ask_size)
        ask_sum = price_list[i] * size_list[i]

        if ask_sum < unfilled_yen:
            unfilled_yen = unfilled_yen - ask_sum
            print("残り：" + str(unfilled_yen))
            i += 1
        else:
            print(price_list)
            print(price_list[-1])
            print(size_list)
            print(size_list[:-1])

            first_size = sum(size_list[:-1])
            unfilled_size = unfilled_yen / float(price_list[-1])
            order_size = round(first_size + unfilled_size, 8)
            print(order_size)
            is_not_done = False
    try:
        order = bf.create_order(symbol='BTC/JPY',
                                type='market',
                                side='buy',
                                amount=order_size,
                                params={"product_code": "BTC_JPY"}
                                )
        print(order)
        return order
    except Exception as e:
        print(e)
        return str(e)
