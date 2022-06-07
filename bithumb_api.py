import requests
import time

khlee_api_key = '85ebe5e7ed02046a072ed94b77e0ba5c'
khlee_scret_key = '14a0e0bb3c7724d76a169340f414a42c'


def get_orderbook_bithumb_timestamp(ticker, timestamp):
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''

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
    if timestamp == rj['data']['timestamp']:
        time.sleep(0.1)
        return -1
    else:
        bithumb_timestamp = rj['data']['timestamp']

    return rj, timestamp


def get_orderbook_bithumb(ticker):
    '''
    :param ticker:
    :return:
        print(result[0]['orderbook_units'][0]['ask_price'])
        print(result[0]['orderbook_units'][0]['bid_price'])
    '''
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

    return rj