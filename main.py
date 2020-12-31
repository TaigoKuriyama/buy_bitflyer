import os

import ccxt

bf = ccxt.bitflyer()
bf.apiKey = os.environ.get("api_key", None)
bf.secret = os.environ.get("api_secret", None)
AMT_BUY = int(os.environ.get("amt_yen", None))


def get_order_size(orderbook, unfilled_yen):
    """ determine order size by amount of JPY """
    i = 0
    price_list = []
    size_list = []
    while True:
        best_ask_price = float(orderbook['asks'][i][0])
        best_ask_size = float(orderbook['asks'][i][1])
        price_list.append(best_ask_price)
        size_list.append(best_ask_size)
        ask_sum = price_list[i] * size_list[i]
        if ask_sum < unfilled_yen:
            unfilled_yen = unfilled_yen - ask_sum
            i += 1
        else:
            first_size = sum(size_list[:-1])
            unfilled_size = unfilled_yen / float(price_list[-1])
            order_size = round(first_size + unfilled_size, 8)
            break
    return order_size


def main(event, context):
    """ order by bitflyer """
    orderbook = bf.fetch_order_book('BTC/JPY')
    unfilled_yen = AMT_BUY
    try:
        order_size = get_order_size(orderbook, unfilled_yen)
        print(f"amount of jpy is {AMT_BUY} yen, order size is {order_size}")
        order = bf.create_order(symbol='BTC/JPY',
                                type='market',
                                side='buy',
                                amount=order_size,
                                params={"product_code": "BTC_JPY"}
                                )
        print("order is done")
        return order
    except Exception as e:
        print(e)
        return str(e)
