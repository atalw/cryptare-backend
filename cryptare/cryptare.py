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
    # update_current_bitcoin_price()
    update_exchanges()


def update_exchanges():
    # update_zebpay_price()
    # update_localbitcoins_price()
    # update_coinsecure_price()
    # update_pocketbits_price()
    # update_throughbit_price()
    # update_koinex_price()
    # update_coinbase_price()
    update_kraken_price()
    # # update_poloniex_price()
    # update_gemini_price()
    # update_bitfinex_price()
    # update_bitstamp_price()
    # update_bittrex_price()

###################################################




def update_poloniex_price():
    prices = get_poloniex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("poloniex_price").push(data)
    else:
        print("poloniex error")


def update_gemini_price():
    prices = get_gemini_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("gemini_price").push(data)
    else:
        print("gemini error")

def update_bitfinex_price():
    prices = get_bitfinex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("bitfinex_price").push(data)
    else:
        print("bitfinex error")

def update_bitstamp_price():
    prices = get_bitstamp_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("bitstamp_price").push(data)
    else:
        print("bitstamp error")

def update_bittrex_price():
    prices = get_bittrex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("bittrex_price").push(data)
    else:
        print("bittrex error")

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



def get_current_bitcoin_price(currency):
    url = "https://api.coindesk.com/v1/bpi/currentprice/{}.json".format(currency)
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        price = json["bpi"][currency]["rate_float"]
        return price
    return None


###################################################

###################################################

def update_zebpay_price():
    prices = get_zebpay_price()
    if prices is not None:
        buy_price, sell_price, vol_24hrs = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price, "vol_24hrs": vol_24hrs}
        db.child("zebpay").push(data)
    else:
        print("zebpay error")


def get_zebpay_price():
    url = "https://api.zebpay.com/api/v1/ticker?currencyCode=INR"
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["buy"]
        sell_price = json["sell"]
        vol_24hrs = json["volume"]

        if buy_price is not None and sell_price is not None and vol_24hrs is not None:
            return buy_price, sell_price, vol_24hrs
    return None

###################################################

###################################################


def update_koinex_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
    # make only 1 API call to koinex
    result = get_koinex_price(coins)
    if result is not None:
        for coin in coins:
            data = {"timestamp": time.time(), "buy_price": result[coin]['buy_price'], "sell_price": result[coin]['sell_price'], "vol_24hrs": result[coin]['vol_24hrs'],
                "max_24hrs": result[coin]['max_24hrs'], "min_24hrs": result[coin]['min_24hrs']}
            db.child("koinex_{}_INR".format(coin)).push(data)
    else:
        print("koinex error")

def get_koinex_price(coins):
    url = "https://koinex.in/api/ticker"
    data = {}
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()

        for coin in coins:
            data[coin] = {}
            data[coin]['buy_price'] = float(json["stats"][coin]["lowest_ask"])
            data[coin]['sell_price'] = float(json["stats"][coin]["highest_bid"])
            data[coin]['vol_24hrs'] = float(json["stats"][coin]["vol_24hrs"])
            data[coin]['max_24hrs'] = float(json["stats"][coin]["max_24hrs"])
            data[coin]['min_24hrs'] = float(json["stats"][coin]["min_24hrs"])

        if data is not None:
            return data
    return None


###################################################


def update_localbitcoins_price():
    # JPY currency not available
    currencies = ["INR", "USD", "GBP", "CNY", "SGD", "EUR", "ZAR"]

    for currency in currencies:
        prices = get_localbitcoins_price(currency)
        if prices is not None:
            buy_price, sell_price, vol_24hrs = prices
            data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price, "vol_24hrs": vol_24hrs}
            title = "localbitcoins_BTC_{}".format(currency)
            db.child(title).push(data)
        else:
            print("localbitcoins error")

def get_localbitcoins_price(currency):
    buy_url = "https://localbitcoins.com/buy-bitcoins-online/{}/.json".format(currency)
    sell_url = "https://localbitcoins.com/sell-bitcoins-online/{}/c/bank-transfers/.json".format(currency)
    volume_url = "https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/"

    buy_request = requests.get(buy_url)
    if buy_request.status_code == 200:
        json = buy_request.json()
        buy_price = json["data"]["ad_list"][0]["data"]["temp_price"]

        sell_request = requests.get(sell_url)
        if sell_request.status_code == 200:
            json = sell_request.json()
            sell_price = json["data"]["ad_list"][0]["data"]["temp_price"]

            volume_request = requests.get(volume_url)
            json = volume_request.json()
            vol_24hrs = json[currency]["volume_btc"]

            if buy_price is not None and sell_price is not None and vol_24hrs is not None:
                buy_price = float(buy_price)
                sell_price = float(sell_price)
                vol_24hrs = float(vol_24hrs)
                return buy_price, sell_price, vol_24hrs
    return None


###################################################

def update_coinsecure_price():
    result = get_coinsecure_price()
    if result is not None:
        data = {"timestamp": time.time(), "buy_price": result[0], "sell_price": result[1], "max_24hrs": result[2],
                "min_24hrs": result[3], "fiat_volume_24hrs": result[4], "coin_volume_24hrs": result[5]}
        db.child("coinsecure").push(data)
    else:
        print("coinsecure error")

def get_coinsecure_price():
    url = "https://api.coinsecure.in/v1/exchange/ticker"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        # does not return 404 if json not found
        if json["success"]:
            buy_price_in_paisa = json["message"]["ask"]
            buy_price = buy_price_in_paisa/100

            sell_price_in_paisa = json["message"]["bid"]
            sell_price = sell_price_in_paisa/100

            max_24hrs_in_paisa = json["message"]["high"]
            max_24hrs = max_24hrs_in_paisa/100

            min_24hrs_in_paisa = json["message"]["low"]
            min_24hrs = min_24hrs_in_paisa/100

            fiat_volume_in_paisa = json["message"]["fiatvolume"]
            fiat_volume_24hrs = fiat_volume_in_paisa/100

            coin_volume = json["message"]["coinvolume"]
            coin_volume_24hrs = coin_volume/100000000

            if buy_price is not None and sell_price is not None and max_24hrs is not None \
                    and min_24hrs is not None and fiat_volume_24hrs is not None and coin_volume_24hrs is not None:
                return [buy_price, sell_price, max_24hrs, min_24hrs, fiat_volume_24hrs, coin_volume_24hrs]
    return None

###################################################


def update_pocketbits_price():
    prices = get_pocketbits_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("pocketbits").push(data)
    else:
        print("pockebits error")


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


###################################################


def update_throughbit_price():
    prices = get_throughbit_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("throughtbit_price").push(data)
    else:
        print("throughbit error")

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


###################################################


def update_coinbase_price():
    coins = ["BTC", "ETH", "LTC"]
    for coin in coins:
        if coin == "ETH" or coin == "LTC":
            currencies = ["USD", "EUR"]
        else:
            currencies = ["USD", "GBP", "EUR"]
        for currency in currencies:
            prices = get_coinbase_price(coin, currency)
            stats = get_gdax_market_stats(coin, currency)
            if prices is not None and stats is not None:
                buy_price, sell_price = prices
                data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price, "max_24hrs": stats[0],
                        "min_24hrs": stats[1], "vol_24hrs": stats[2], "vol_30days": stats[3]}
                db.child("coinbase_{0}_{1}".format(coin, currency)).push(data)
            else:
                print("coinbase error")


def get_coinbase_price(coin, currency):
    buy_url = "https://api.coinbase.com/v2/prices/{0}-{1}/buy".format(coin, currency)
    sell_url = "https://api.coinbase.com/v2/prices/{0}-{1}/sell".format(coin, currency)

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


def get_gdax_market_stats(coin, currency):
    url = "https://api.gdax.com/products/{0}-{1}/stats".format(coin, currency)

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        max_24hrs = json["high"]
        min_24hrs = json["low"]
        vol_24hrs = json["volume"]
        vol_30days = json["volume_30day"]

        if max_24hrs is not None and min_24hrs is not None and vol_24hrs is not None and vol_30days is not None:
            return [float(max_24hrs), float(min_24hrs), float(vol_24hrs), float(vol_30days)]

###################################################


def update_kraken_price():
    coins = ["BTC", "LTC", "ETH"]
    for coin in coins:
        if coin == "LTC":
            currencies = ["USD", "EUR"]
        else:
            currencies = ["USD", "GBP", "JPY", "CAD", "EUR"]
        for currency in currencies:
            result = get_kraken_price(coin, currency)
            if result is not None:
                data = {"timestamp": time.time(), "buy_price": result[0], "sell_price": result[1],
                        "vol_24hrs": result[2], "max_24hrs": result[3], "min_24hrs": result[4]}
                db.child("kraken_{0}_{1}".format(coin, currency)).push(data)
            else:
                print("kraken error")


def get_kraken_price(coin, currency):
    if coin == "BTC":
        coin = "XBT"
    url = "https://api.kraken.com/0/public/Ticker?pair={0}{1}".format(coin, currency)

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        coin_currency_pair = "X{0}Z{1}".format(coin, currency)
        buy_price = json["result"][coin_currency_pair]["a"][0]
        sell_price = json["result"][coin_currency_pair]["b"][0]
        vol_24hrs = json["result"][coin_currency_pair]["v"][1]
        max_24hrs = json["result"][coin_currency_pair]["h"][1]
        min_24hrs = json["result"][coin_currency_pair]["l"][1]

        if buy_price is not None and sell_price is not None and vol_24hrs is not None and \
                        max_24hrs is not None and min_24hrs is not None:
            return [buy_price, sell_price, vol_24hrs, max_24hrs, min_24hrs]
    return None


###################################################

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
        buy_price = json["ask"]
        sell_price = json["bid"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

def get_bitfinex_price():
    url =  "https://api.bitfinex.com/v1/pubticker/btcusd"

    r = requests.get(url)
    if r.status_code == 200:
        if r.headers['Content-Type'] == 'application/json; charset=utf-8':
            json = r.json()
            buy_price = json["ask"]
            sell_price = json["bid"]

            if buy_price is not None and sell_price is not None:
                return buy_price, sell_price
    return None

def get_bitstamp_price():
    url = "https://www.bitstamp.net/api/ticker/"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["ask"]
        sell_price = json["bid"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

def get_bittrex_price():
    url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        buy_price = json["result"]["Ask"]
        sell_price = json["result"]["Bid"]

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

###################################################

execute()
