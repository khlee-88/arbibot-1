import requests
from pprint import pprint
import time
import telegram
import os
import platform

os_info = platform.system()
bot_token = '5275329854:AAHBR7xbp4-eWYMHpDRwXk6uPLw1DTXUISU'

bot = telegram.Bot(bot_token)
chat_id = -1001680607397
chat_id_khlee = 973992508

kobit_timestamp = 0


def get_orderbook_kobit(ticker):
    global kobit_timestamp
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''
    # 'xrp_krw'
    url = "https://api.korbit.co.kr/v1/orderbook"
    headers = {"currency_pair": ticker}
    try:
        response = requests.request("GET", url, params=headers)
    except:
        return -1
    try:
        rj = response.json()
    except:
        return -1
    try:
        te = rj['bids']
    except:
        return -1
    if kobit_timestamp == rj['timestamp']:
        time.sleep(0.1)
        return -1
    else:
        kobit_timestamp = rj['timestamp']

    return rj


upbit_timestamp = 0


def get_orderbook_upbit(ticker):
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''
    global upbit_timestamp
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
    try:
        te = rj[0]['orderbook_units']
    except:
        return -1
    if upbit_timestamp == rj[0]['timestamp']:
        time.sleep(0.1)
        return -1
    else:
        upbit_timestamp = rj[0]['timestamp']
    return rj


bithumb_timestamp = 0
def get_orderbook_bithumb(ticker):
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''
    global bithumb_timestamp
    url = f"https://api.bithumb.com/public/orderbook/{ticker}"
    try:
        response = requests.get(url)
    except:
        return -1
    try:
        rj = response.json()
    except:
        return -1
    try:
        te = rj['data']['asks'][0]
    except:
        return -1
    if bithumb_timestamp == rj['data']['timestamp']:
        time.sleep(0.1)
        return -1
    else:
        bithumb_timestamp = rj['data']['timestamp']

    return rj


coinone_timestamp = 0


def get_orderbook_coinone(ticker, payment):
    global coinone_timestamp
    url = f'https://api.coinone.co.kr/public/v2/orderbook/{payment}/{ticker}'
    try:
        response = requests.get(url)
    except:
        return -1
    try:
        rj = response.json()
    except:
        return -1
    try:
        te = rj['bids']
    except:
        return -1
    if coinone_timestamp == rj['timestamp']:
        time.sleep(0.1)
        return -1
    else:
        coinone_timestamp = rj['timestamp']

    return rj


error_cnt = 0
virtual_amount_bithumb = 0
virtual_amount_coinone = 0
today_balancing_count = 0
ticker = "XRP"

while True:
    error_cnt += 1
    if error_cnt >= 100:
        bot.sendMessage(chat_id=chat_id, text="error is too much")
        error_cnt = 0

    res = requests.get("https://api.bithumb.com/public/orderbook/XRP_KRW")
    bithumb_orderbooks = get_orderbook_bithumb("XRP_KRW")
    if bithumb_orderbooks == -1:
        continue
    try:
        bithumb_ask_price = float(bithumb_orderbooks['data']['asks'][0]['price'])
        bithumb_ask_quantity = float(bithumb_orderbooks['data']['asks'][0]['quantity'])
        bithumb_bid_price = float(bithumb_orderbooks['data']['bids'][0]['price'])
        bithumb_bid_quantity = float(bithumb_orderbooks['data']['bids'][0]['quantity'])
    except:
        continue

    coinone_orderbooks = get_orderbook_coinone("XRP", "KRW")
    if coinone_orderbooks == -1:
        continue
    try:
        coinone_ask_price = float(coinone_orderbooks['asks'][0]['price'])
        coinone_ask_quantity = float(coinone_orderbooks['asks'][0]['qty'])
        coinone_bid_price = float(coinone_orderbooks['bids'][0]['price'])
        coinone_bid_quantity = float(coinone_orderbooks['bids'][0]['qty'])
    except:
        continue

    # kobit_orderbooks = get_orderbook_kobit("xrp_krw")
    # if kobit_orderbooks == -1:
    #     continue
    # try:
    #     kobit_ask_price = float(kobit_orderbooks['asks'][0][0])
    #     kobit_ask_quantity = float(kobit_orderbooks['asks'][0][1])
    #     kobit_bid_price = float(kobit_orderbooks['bids'][0][0])
    #     kobit_bid_quantity = float(kobit_orderbooks['bids'][0][1])
    # except:
    #     continue

    # ask 매수
    # bid 매도

    upbit_orderbooks = get_orderbook_upbit("KRW-XRP")
    if upbit_orderbooks == -1:
        continue
    try:
        upbit_ask_price = float(upbit_orderbooks[0]['orderbook_units'][0]['ask_price'])
        upbit_ask_quantity = float(upbit_orderbooks[0]['orderbook_units'][0]['ask_size'])

        upbit_bid_price = float(upbit_orderbooks[0]['orderbook_units'][0]['bid_price'])
        upbit_bid_quantity = float(upbit_orderbooks[0]['orderbook_units'][0]['bid_size'])
    except:
        continue

    # bu_spread = float(bithumb_bid_price) - float(upbit_ask_price)
    ub_spread = upbit_bid_price - bithumb_ask_price
    uc_spread = upbit_bid_price - coinone_ask_price
    # uk_spread = upbit_bid_price - kobit_ask_price

    bu_spread = bithumb_bid_price - upbit_ask_price
    cu_spread = coinone_bid_price - upbit_ask_price
    # ku_spread = kobit_bid_price - upbit_ask_price

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
    # bid = 지금 팔 수 있는 가격, ask = 지금 살 수 있는 가격
    # print(f"비교 가격(upbit bid - bithumb ask) : {upbit_bid_price}, {bithumb_ask_price}, {ub_spread}")
    # print(f"비교 가격(upbit bid - coinone ask) : {upbit_bid_price}, {coinone_ask_price}, {uc_spread}")
    # print(f"비교 가격(upbit bid - kobit ask) : {upbit_bid_price}, {kobit_ask_price}, {uk_spread}")
    # print()
    # print(f"비교 가격_reverse(bithumb bid - upbit ask) : {bithumb_bid_price}, {upbit_ask_price}, {bu_spread}")
    # print(f"비교 가격_reverse(coinone bid - upbit ask) : {coinone_bid_price}, {upbit_ask_price}, {cu_spread}")
    # print(f"비교 가격(kobit bid - upbit ask) : {kobit_bid_price}, {upbit_ask_price}, {ku_spread}")
    # print()



    if ub_spread >= 1:
        if upbit_ask_quantity > bithumb_bid_quantity:
            virtual_amount_bithumb += bithumb_bid_quantity / 3
        elif bithumb_bid_quantity > upbit_ask_quantity:
            virtual_amount_bithumb += upbit_ask_quantity / 3
        # print(f"비교 가격(upbit bid - bithumb ask) : {ub_spread}\n"
        #                                       f"u_bid={upbit_bid_price}\nb_ask={bithumb_ask_price}\n"
        #                                       f"u_size={upbit_bid_quantity}\nb_size={bithumb_ask_quantity}\n"
        #                                       f"virtual_amount={virtual_amount}")
        bot.sendMessage(chat_id=chat_id_khlee, text=f"비교 가격(upbit bid - bithumb ask) : {ub_spread}\n"
                                              f"u_bid={upbit_bid_price}\nb_ask={bithumb_ask_price}\n"
                                              f"u_size={upbit_bid_quantity}\nb_size={bithumb_ask_quantity}\n"
                                              f"virtual_amount={virtual_amount_bithumb}")
    if virtual_amount_bithumb >= 40000:
        today_balancing_count += 1
        bot.sendMessage(chat_id=chat_id_khlee, text=f"Need Balancing:{today_balancing_count}")
        virtual_amount_bithumb = 0

    if uc_spread >= 1.3:
        # if upbit_bid_quantity > coinone_ask_quantity:
        #     virtual_amount_bithumb += coinone_ask_quantity / 3
        # elif coinone_ask_quantity > upbit_bid_quantity:
        #     virtual_amount_bithumb += upbit_bid_quantity / 3
        # print(f"비교 가격(upbit bid - coinone ask) : {uc_spread}\n"
        #                                       f"u_bid={upbit_bid_price}\nc_ask={coinone_ask_price}\n"
        #                                       f"u_size={upbit_bid_quantity}\nc_size={coinone_ask_quantity}\n"
        #                                       f"virtual_amount={virtual_amount}")
        bot.sendMessage(chat_id=chat_id, text=f"비교 가격(upbit bid - coinone ask) : {uc_spread}\n"
                                              f"u_bid={upbit_bid_price}\nc_ask={coinone_ask_price}\n"
                                              f"u_size={upbit_bid_quantity}\nc_size={coinone_ask_quantity}")

    # if uk_spread >= 2.5:
    #     if upbit_bid_quantity > kobit_ask_quantity:
    #         virtual_amount += kobit_ask_quantity / 3
    #     elif kobit_ask_quantity > upbit_bid_quantity:
    #         virtual_amount += upbit_bid_quantity / 3
    #     print(f"비교 가격(upbit bid - kobit ask) : {uk_spread}\n"
    #                                           f"u_bid={upbit_bid_price}\nk_ask={kobit_ask_price}\n"
    #                                           f"u_size={upbit_bid_quantity}\nk_size={kobit_ask_quantity}\n"
    #                                           f"virtual_amount={virtual_amount}")
    #     bot.sendMessage(chat_id=chat_id, text=f"비교 가격(upbit bid - kobit ask) : {uk_spread}\n"
    #                                           f"u_bid={upbit_bid_price}\nk_ask={kobit_ask_price}\n"
    #                                           f"u_size={upbit_bid_quantity}\nk_size={kobit_ask_quantity}\n"
    #                                           f"virtual_amount={virtual_amount}")

    error_cnt = 0
    time.sleep(3)

# if bu_spread >= 1:
#     if upbit_bid_quantity > bithumb_ask_quantity:
#         virtual_amount += bithumb_ask_quantity / 3
#     elif bithumb_ask_quantity > upbit_bid_quantity:
#         virtual_amount += upbit_bid_quantity / 3
#     print(f"비교 가격(upbit bid - bithumb ask) : {bu_spread}\n"
#                                           f"u_bid={upbit_bid_price}\n b_ask={bithumb_ask_price}\n"
#                                           f"u_size={upbit_bid_quantity}\n b_size={bithumb_ask_quantity}\n"
#                                           f"virtual_amount={virtual_amount}")
#     # bot.sendMessage(chat_id=chat_id, text=f"비교 가격(upbit bid - bithumb ask) : {bu_spread}\n"
#     #                                       f"u_bid={upbit_bid_price}\n b_ask={bithumb_ask_price}\n"
#     #                                       f"u_size={upbit_bid_quantity}\n b_size={bithumb_ask_quantity}\n"
#     #                                       f"virtual_amount={virtual_amount}")
