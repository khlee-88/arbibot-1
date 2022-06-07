import requests
from pprint import pprint
import time
import telegram

bot_token = '5275329854:AAHBR7xbp4-eWYMHpDRwXk6uPLw1DTXUISU'

bot = telegram.Bot(bot_token)
chat_id = 973992508

def get_orderbook(ticker):
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''
    url = "https://api.upbit.com/v1/orderbook"
    headers = {"markets": ticker}
    try:
        response = requests.request("GET", url, params=headers)
    except:
        return -1
    try:
        rj = response.json()
    except:
        return -1
    return rj

while True:
    res = requests.get("https://api.bithumb.com/public/orderbook/XRP_KRW")
    bithumb_orderbooks = res.json()
    bithumb_ask_price = bithumb_orderbooks['data']['asks'][0]['price']
    bithumb_ask_quantity = bithumb_orderbooks['data']['asks'][0]['quantity']

    bithumb_bid_price = bithumb_orderbooks['data']['bids'][0]['price']
    bithumb_bid_quantity = bithumb_orderbooks['data']['bids'][0]['quantity']



    upbit_orderbooks = get_orderbook("KRW-XRP")
    upbit_ask_price = upbit_orderbooks[0]['orderbook_units'][0]['ask_price']
    upbit_ask_quantity = upbit_orderbooks[0]['orderbook_units'][0]['ask_size']

    upbit_bid_price = upbit_orderbooks[0]['orderbook_units'][0]['bid_price']
    upbit_bid_quantity = upbit_orderbooks[0]['orderbook_units'][0]['bid_size']

    ub_sprad = float(bithumb_bid_price) - float(upbit_ask_price)
    bu_sprad = float(upbit_bid_price) - float(bithumb_ask_price)

    # print(f"bithumb_ask_price : {bithumb_ask_price}")
    # print(f"bithumb_ask_quantity : {bithumb_ask_quantity}")
    # print(f"bithumb_bid_price : {bithumb_bid_price}")
    # print(f"bithumb_bid_quantity : {bithumb_bid_quantity}")
    #
    # print(f"upbit_ask_price : {upbit_ask_price}")
    # print(f"upbit_ask_quantity : {upbit_ask_quantity}")
    # print(f"upbit_bid_price : {upbit_bid_price}")
    # print(f"upbit_bid_quantity : {upbit_bid_quantity}")
    # print()
    #
    # print(f"비교 가격(bithumb bid - upbit ask) : {upbit_ask_price}, {bithumb_bid_price}, {ub_sprad}")
    # print(f"비교 가격(upbit bid - bithumb ask) : {bithumb_ask_price}, {upbit_bid_price}, {bu_sprad}")
    # print()

    if ub_sprad >= 1:
        bot.sendMessage(chat_id=chat_id, text=f"비교 가격(bithumb bid - upbit ask) : {ub_sprad}\n"
                                              f"b_bid={bithumb_bid_price}\n u_ask={upbit_ask_price}\n"
                                              f"u_size={upbit_ask_quantity}\n b_size={bithumb_bid_quantity}")
    if bu_sprad >= 1:
        bot.sendMessage(chat_id=chat_id, text=f"비교 가격(upbit bid - bithumb ask) : {bu_sprad}\n"
                                              f"u_bid={upbit_bid_price}\n b_ask={bithumb_ask_price}\n"
                                              f"u_size={upbit_bid_quantity}\n b_size={bithumb_ask_quantity}")
    time.sleep(4)