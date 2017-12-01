# -*- coding: utf-8 -*-

import requests
import pyrebase
import time

config = {
  "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
  "authDomain": "atalwcryptare.firebaseapp.com",
  "databaseURL": "https://atalwcryptare.firebaseio.com/",
  "storageBucket": "atalwcryptare.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

currencies = ["INR", "USD"]

###################################################


def update_current_bitcoin_price():
    for currency in currencies:
        price = get_current_bitcoin_price(currency)
        if price is not None:
            # store price and timestamp
            data = {"timestamp": time.time(), "price": price}
            title = "current_btc_price_{}".format(currency)
            db.child(title).push(data)


def update_zebpay_price():
    prices = get_zebpay_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("zebpay_price").push(data)


def update_localbitcoins_price():
    for currency in currencies:
        prices = get_localbitcoins_price(currency)
        if prices is not None:
            buy_price, sell_price = prices
            data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
            title = "localbitcoins_price_{}".format(currency)
            db.child(title).push(data)


def update_coinsecure_price():
    prices = get_coinsecure_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("coinsecure_price").push(data)

def update_pocketbits_price():
    prices = get_pocketbits_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buyPrice": buy_price, "sellPrice": sell_price}
        db.child("pocketbits_price").push(data)


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
    url = "https://api.zebpay.com/api/v1/ticker?cutrencyCode=INR"
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
    url = "https://www.pocketbits.in/Index/getBalaanceRates"

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


# update_current_bitcoin_price()
# update_zebpay_price()
# update_localbitcoins_price()
# update_coinsecure_price()
# update_pocketbits_price()