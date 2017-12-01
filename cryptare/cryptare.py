# -*- coding: utf-8 -*-

import requests
import pyrebase

config = {
  "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
  "authDomain": "atalwcryptare.firebaseapp.com",
  "databaseURL": "https://atalwcryptare.firebaseio.com/",
  "storageBucket": "atalwcryptare.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def update_current_bitcoin_price():
    price = get_current_bitcoin_price("INR")
    db.child("btc").push(price)
    print("pushed")


def get_current_bitcoin_price(currency):
    url = "https://api.coindesk.com/v1/bpi/currentprice/{}.json".format(currency)
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        price = json["bpi"][currency]["rate_float"]
        return price

update_current_bitcoin_price()