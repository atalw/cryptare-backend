# -*- coding: utf-8 -*-

import requests
import pyrebase
import time
import json as jsonmodule

config = {
    "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
    "authDomain": "atalwcryptare.firebaseapp.com",
    "databaseURL": "https://atalwcryptare.firebaseio.com/",
    "storageBucket": "atalwcryptare.appspot.com",
    "serviceAccount": "../service_account_info/Cryptare-9d04b184ba96.json"
}

firebase = pyrebase.initialize_app(config)

# # Get a reference to the auth service
# auth = firebase.auth()
#
# # Log the user in
# user = auth.sign_in_with_email_and_password(sys.argv[1], sys.argv[2])

# Get a reference to the database service
db = firebase.database()

currencies = ["INR", "USD", "GBP", "JPY", "CNY", "SGD", "EUR", "ZAR"]

###################################################

# NOTES

# API update frequency and rate limit wherever applicable
# - Coindesk:
# - Zebpay: apparently updated every 5 minutes lol
# - Localbitcoins:
# - Koinex:
# - Coinsecure:
# - Throughbit
# - Pocketbits:
# - Kraken:
# - Bitfinex:
# - Bittrex:
# - Gemini:
# - Bitstamp:
# - Coinbase:

###################################################


def execute():
    while True:
        update_all()
        time.sleep(60)

def update_all():
    update_current_bitcoin_price()
    update_exchanges()


def update_exchanges():
    update_zebpay_price()
    update_localbitcoins_price()
    update_coinsecure_price()
    update_pocketbits_price()
    # update_throughbit_price()
    update_koinex_price()
    update_coinbase_price()
    update_kraken_price()
    # update_poloniex_price()
    update_gemini_price()
    update_bitfinex_price()
    update_bitstamp_price()
    update_bittrex_price()

###################################################


def update_current_bitcoin_price():
    for currency in currencies:
        price = get_current_bitcoin_price(currency)
        if price is not None:
            # store price and timestamp
            data = {"timestamp": time.time(), "price": price}
            title = "current_btc_price_{}".format(currency)
            db.child(title).push(data)
        else:
            print("current btc error")


def update_zebpay_price():
    prices = get_zebpay_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("zebpay_price").push(data)
    else:
        print("zebpay error")


def update_localbitcoins_price():
    for currency in currencies:
        prices = get_localbitcoins_price(currency)
        if prices is not None:
            buy_price, sell_price = prices
            data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
            title = "localbitcoins_price_{}".format(currency)
            db.child(title).push(data)
        else:
            print("localbitcoins error")


def update_coinsecure_price():
    prices = get_coinsecure_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("coinsecure_price").push(data)
    else:
        print("coinsecure error")


def update_pocketbits_price():
    prices = get_pocketbits_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("pocketbits_price").push(data)
    else:
        print("pockebits error")


def update_throughbit_price():
    prices = get_throughbit_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("throughtbit_price").push(data)
    else:
        print("throughbit error")


def update_koinex_price():
    prices = get_koinex_price()
    if prices is not None:
        buy_price, sell_price, day_volume = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price, "24hVolume": day_volume}
        db.child("koinex_price").push(data)
    else:
        print("koinex error")


def update_coinbase_price():
    prices = get_coinbase_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("coinbase_price").push(data)
    else:
        print("coinbase error")


def update_kraken_price():
    prices = get_kraken_price()
    if prices is not None:
        buy_price, sell_price, day_volume = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price, "24hVolume": day_volume}
        db.child("kraken_price").push(data)
    else:
        print("kraken error")


def update_poloniex_price():
    prices = get_poloniex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("poloniex_price").push(data)
    else:
        print("poloniex error")


def update_gemini_price():
    prices = get_gemini_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("gemini_price").push(data)
    else:
        print("gemini error")

def update_bitfinex_price():
    prices = get_bitfinex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("bitfinex_price").push(data)
    else:
        print("bitfinex error")

def update_bitstamp_price():
    prices = get_bitstamp_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("bitstamp_price").push(data)
    else:
        print("bitstamp error")

def update_bittrex_price():
    prices = get_bittrex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("bittrex_price").push(data)
    else:
        print("bittrex error")

###################################################


def get_current_bitcoin_price(currency):
    url = "https://api.coindesk.com/v1/bpi/currentprice/{}.json".format(currency)
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        price = json["bpi"][currency]["rate_float"]
        return price
    return None


def get_zebpay_price():
    url = "https://api.zebpay.com/api/v1/ticker?currencyCode=INR"
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["buy"]
        sell_price = json["sell"]
        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None


def get_localbitcoins_price(currency):
    buy_url = "https://localbitcoins.com/buy-bitcoins-online/{}/.json".format(currency)
    sell_url = "https://localbitcoins.com/sell-bitcoins-online/{}/c/bank-transfers/.json".format(currency)

    buy_request = requests.get(buy_url)
    if buy_request.status_code == 200:
        json = buy_request.json()
        buy_price = json["data"]["ad_list"][0]["data"]["temp_price"]

        sell_request = requests.get(sell_url)
        if sell_request.status_code == 200:
            json = sell_request.json()
            sell_price = json["data"]["ad_list"][0]["data"]["temp_price"]

            if buy_price is not None and sell_price is not None:
                buy_price = float(buy_price)
                sell_price = float(sell_price)
                return buy_price, sell_price
    return None


def get_coinsecure_price():
    url = "https://api.coinsecure.in/v1/exchange/ticker"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        # does not return 404 if json not found
        if json["success"]:
            buy_price_in_paisa = json["message"]["bid"]
            sell_price_in_paisa = json["message"]["ask"]
            return buy_price_in_paisa/100, sell_price_in_paisa/100
    return None

def get_pocketbits_price():
    url = "https://www.pocketbits.in/Index/getBalanceRates"

    r = requests.get(url)
    if r.status_code == 200:
        if r.headers["Content-Type"] == "application/json; charset=utf-8":
            json = r.json()
            buy_price = json["rates"]["BTC_BuyingRate"]
            sell_price = json["rates"]["BTC_SellingRate"]

            if buy_price is not None and sell_price is not None:
                return buy_price, sell_price
    return None

def get_throughbit_price():
    url = "https://www.throughbit.com/tbit_ci/index.php/cryptoprice/type/btc/inr"
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
               'cookie': 'visid_incap_1176184=43563B0yS265oyLWGgZmNHRoIVoAAAAAQkIPAAAAAACAeZKAAWdNAOaK1XaaEDa257oj3KMxGCxy; incap_ses_873_1176184=olb7HICRaAM5r3L69IQdDFxUIloAAAAAyEpHFyG4srGo6Xg1Vh/fDw==; io=PhOhELHW7WLVJGmVD9OO'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        json = jsonmodule.loads(r.text)
        buy_price = json["data"]["price"][0]["buy_price"]
        sell_price = json["data"]["price"][0]["sell_price"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None


def get_koinex_price():
    url = "https://koinex.in/api/ticker"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = float(json["stats"]["BTC"]["highest_bid"])
        sell_price = float(json["stats"]["BTC"]["lowest_ask"])
        day_volume = float(json["stats"]["BTC"]["vol_24hrs"])

        if buy_price is not None and sell_price is not None and day_volume is not None:
            return buy_price, sell_price, day_volume
    return None

def get_coinbase_price():
    buy_url = "https://api.coinbase.com/v2/prices/BTC-USD/buy"
    sell_url = "https://api.coinbase.com/v2/prices/BTC-USD/sell"

    buy_request = requests.get(buy_url)
    if buy_request.status_code == 200:
        json = buy_request.json()
        buy_price = json["data"]["amount"]

        sell_request = requests.get(sell_url)
        if sell_request.status_code == 200:
            json = sell_request.json()
            sell_price = json["data"]["amount"]

            if buy_price is not None and sell_price is not None:
                return buy_price, sell_price
    return None


def get_kraken_price():
    url = "https://api.kraken.com/0/public/Ticker?pair=xbtusd"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["result"]["XXBTZUSD"]["a"][0]
        sell_price = json["result"]["XXBTZUSD"]["b"][0]
        day_volume = json["result"]["XXBTZUSD"]["v"][1]

        if buy_price is not None and sell_price is not None and day_volume is not None:
            return buy_price, sell_price, day_volume
    return None


def get_poloniex_price():
    url = "https://poloniex.com/public?command=returnTicker"
    # workaround - cookie expires on 1st Dec 2018
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
                'cookie': '__cfduid=d8b5b9d7ee920012a5de62f760368aeb31512142306; POLOSESSID=fsfqn9tseg0foclkll5sj14s20; cf_clearance=77cc2cdc7d2dc2ea346c639fb05d6f0e0d76485e-1512195307-1800'}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["USDT_BTC"]["lowestAsk"]
        sell_price = json["USDT_BTC"]["highestBid"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

def get_gemini_price():
    url = "https://api.gemini.com/v1/pubticker/btcusd"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["bid"]
        sell_price = json["ask"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

def get_bitfinex_price():
    url =  "https://api.bitfinex.com/v1/pubticker/btcusd"

    r = requests.get(url)
    if r.status_code == 200:
        if r.headers['Content-Type'] == 'application/json; charset=utf-8':
            json = r.json()
            buy_price = json["bid"]
            sell_price = json["ask"]

            if buy_price is not None and sell_price is not None:
                return buy_price, sell_price
    return None

def get_bitstamp_price():
    url = "https://www.bitstamp.net/api/ticker/"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["bid"]
        sell_price = json["ask"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

def get_bittrex_price():
    url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["result"]["Bid"]
        sell_price = json["result"]["Ask"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

###################################################

execute()
