import requests
import json
from pprint import pprint
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import platform
import time

server_url = 'https://api.upbit.com'


def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time - start_time))
        return result

    return wrapper_fn


def get_price(ticker):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": ticker, "count": "1"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    jres = response.json()
    return jres


def get_trade_price(ticker):
    '''
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":ticker,"count":"1"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    jres = response.json()
    return jres[0]['trade_price']
    '''
    url = "https://api.upbit.com/v1/trades/ticks"
    # querystring = {"count": "1"}
    headers = {"market": ticker}
    try:
        response = requests.request("GET", url, params=headers)
    except Exception as e:
        print(f"something error : {response.test}, {e}")
        return -1

    try:
        ret = response.json()
    except Exception as e:
        print(f"json error : {e}")
        return -1
    # pprint(ret)
    return ret[0]['trade_price']


def get_trade_price_threading(tickers):
    '''
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":ticker,"count":"1"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    jres = response.json()
    return jres[0]['trade_price']
    '''
    url = "https://api.upbit.com/v1/trades/ticks"
    # querystring = {"count": "1"}
    headers = {"market": tickers}
    response = requests.request("GET", url, params=headers)
    ret = response.json()
    # pprint(ret)
    return ret[0]['trade_price']


def get_key():
    with open("./upbit_key.txt") as f:
        lines = f.readlines()
        global access_key
        global secret_key
        access_key = lines[1].strip()
        secret_key = lines[3].strip()
        # return api_key, secret_key


def get_balance():
    get_key()
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    try:
        res = requests.get(server_url + "/v1/accounts", headers=headers, timeout=2)
    except:
        return -1
    try:
        ret = res.json()
    except:
        return -1
    return ret


def get_balance_for_telegram():
    get_key()
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url + "/v1/accounts", headers=headers)
    rjson = res.json()
    position_list = list()

    for i in rjson:
        if i['currency'] != 'KRW':
            position_list.append(f"{i['currency']} : {i['balance']}")

    return position_list


def get_balance_ticker(ticker):
    get_key()
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),

    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')

    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    try:
        res = requests.get(server_url + "/v1/accounts", headers=headers)
    except:
        return -1
    try:
        balance = res.json()
    except:
        return -1
    ret = 0
    try:
        for i in balance:
            if i['currency'] == ticker:
                ret = i['balance']
    except:
        return -1
    return float(ret)


def get_order_chance(ticker):
    get_key()
    query = {
        'market': ticker,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
    return res.json()


def order_market_buy(ticker, price):
    get_key()
    query = {
        'market': ticker,
        'side': 'bid',
        'price': price,
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    return res.json()


def order_market_sell(ticker, volume):
    get_key()
    query = {
        'market': ticker,
        'side': 'ask',
        'volume': volume,
        'ord_type': 'market',
    }
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    return res.json()


def order_list(uuids):
    get_key()
    query = {
        'uuid': uuids,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/order", params=query, headers=headers)
    return res.json()


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


def get_orderbook_match(ticker):
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

def withdraw_krw(amount):
    get_key()
    query = {
        'amount': amount,
    }
    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/withdraws/krw", params=query, headers=headers)
    return res.json()


if __name__ == "__main__":
    # ret = order_market_sell("KRW-ETH", 0.00398089)
    print("run")
    # print(ret)
    # get_key()
    # print(access_key)
    # print(secret_key)


