# -*- coding: utf-8 -*-
#!/usr/bin/python3

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

coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "NEO", "GAS", "XLM", "DASH", "OMG",
         "QTUM", "REQ", "ZRX", "GNT", "BAT", "AE", "RPX", "DBC", "XMR", "DOGE",
         "SIA", "TRX", "DGB", "ZEC", "BTG", "IOT"]

currencies = ["INR", "USD", "GBP", "CAD","JPY", "CNY", "SGD", "EUR", "ZAR", "AUD"]

all_markets = {}

all_exchange_prices = {}

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
    for coin in coins:
        all_exchange_prices[coin] = {}
        for currency in currencies:
            all_exchange_prices[coin][currency] = []
    update_exchanges()
    update_average_price()


def update_exchanges():
    update_zebpay_price()
    update_localbitcoins_price()
    update_coinsecure_price()
    update_pocketbits_price()
    update_koinex_price()
    update_throughbit_price()
    update_bitbns_price()
    update_coinome_price()
    update_coindelta_price()

    update_coinbase_price()
    update_kraken_price()
    # update_poloniex_price()
    update_gemini_price()
    update_bitfinex_price()
    update_bitstamp_price()
    # update_bittrex_price()

    update_kucoin_price()

    update_markets()

###################################################


def update_average_price():
    average_prices = {}
    for coin in coins:
        average_prices[coin] = {}
        for currency in currencies:
            total_sum = sum(all_exchange_prices[coin][currency])
            if len(all_exchange_prices[coin][currency]) > 0:
                average = total_sum/len(all_exchange_prices[coin][currency])
                average_prices[coin][currency] = average
                db.child(coin).child("Data").child(currency).update({"price": average, "timestamp": time.time()})
            else:
                average_prices[coin][currency] = 0

def update_24hr_change(current_price, min_24hr_price, coin):
    change = current_price - min_24hr_price
    percent = change / min_24hr_price * 100
    rounded_percentage = round(percent, 2)
    # db.child(coin).child("Data").child("INR").update({"change_24hrs_percent": rounded_percentage, "change_24hrs_fiat": change})


###################################################


def update_zebpay_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
    result = get_zebpay_price(coins)
    if result is not None:
        for coin in coins:
            data = {"timestamp": time.time(), "last_price": result[coin]["last_price"] ,"buy_price": result[coin]["buy_price"],
                    "sell_price": result[coin]["sell_price"], "vol_24hrs": result[coin]["vol_24hrs"]}
            db.child("zebpay_new/{}/INR".format(coin)).push(data)
            if coin == "BTC": #support old version of cryptare
                db.child("zebpay").push(data)
            all_exchange_prices[coin]["INR"].append(result[coin]["last_price"])
            add_market_entry(coin, 'INR', 'Zebpay', 'zebpay_new')
    else:
        print("zebpay error")


def get_zebpay_price(coins):
    data = {}
    for coin in coins:
        url = "https://www.zebapi.com/api/v1/market/ticker-new/{}/inr".format(coin.lower())
        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            data[coin] = {}
            try:
                data[coin]["last_price"] = json["market"]
                data[coin]["buy_price"]= json["buy"]
                data[coin]["sell_price"] = json["sell"]
                data[coin]["vol_24hrs"] = json["volume"]
            except:
                return None

    if data is not None:
        return data
    return None

###################################################


def update_koinex_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "OMG", "REQ", "ZRX", "GNT", "BAT",
             "AE", "TRX", "XLM", "NEO", "GAS"]
    # make only 1 API call to koinex
    result = get_koinex_price(coins)
    if result is not None:
        for coin in coins:
            data = {"timestamp": time.time(), "last_price": result[coin]['last_price'], "buy_price": result[coin]['buy_price'], "sell_price": result[coin]['sell_price'], "vol_24hrs": result[coin]['vol_24hrs'],
                "max_24hrs": result[coin]['max_24hrs'], "min_24hrs": result[coin]['min_24hrs']}
            db.child("koinex/{}/INR".format(coin)).push(data)
            add_market_entry(coin, 'INR', 'Koinex', 'koinex')
            all_exchange_prices[coin]["INR"].append(result[coin]['last_price'])
            update_24hr_change(result[coin]['last_price'], result[coin]['min_24hrs'], coin)
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
            try:
                data[coin]['last_price'] = float(json["stats"][coin]["last_traded_price"])
                data[coin]['buy_price'] = float(json["stats"][coin]["lowest_ask"])
                data[coin]['sell_price'] = float(json["stats"][coin]["highest_bid"])
                data[coin]['vol_24hrs'] = float(json["stats"][coin]["vol_24hrs"])
                data[coin]['max_24hrs'] = float(json["stats"][coin]["max_24hrs"])
                data[coin]['min_24hrs'] = float(json["stats"][coin]["min_24hrs"])
            except:
                return None

        if data is not None:
            return data
    return None


###################################################


def update_localbitcoins_price():
    # JPY currency not available
    currencies = ["INR", "USD", "GBP", "CNY", "SGD", "EUR", "ZAR"]

    volume_data = get_localbitcoins_volume(currencies)
    for currency in currencies:
        prices = get_localbitcoins_price(currency)
        if prices is not None and volume_data is not None:
            buy_price, sell_price = prices
            data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price, "vol_24hrs": volume_data[currency]}
            title = "localbitcoins/BTC/{}".format(currency)
            db.child(title).push(data)
            add_market_entry('BTC', currency, 'Localbitcoins', 'localbitcoins')
            all_exchange_prices["BTC"][currency].append(buy_price)
        else:
            print("localbitcoins error")

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

def get_localbitcoins_volume(currencies):
    volume_url = "https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/"
    data = {}
    volume_request = requests.get(volume_url)
    if volume_request.status_code == 200:
        json = volume_request.json()
        for currency in currencies:
            try:
                vol_24hrs = json[currency]["volume_btc"]
            except:
                return None

            if vol_24hrs is not None:
                data[currency] = float(vol_24hrs)
        return data
    return None

###################################################

def update_coinsecure_price():
    result = get_coinsecure_price()
    if result is not None:
        data = {"timestamp": time.time(), "buy_price": result[0], "sell_price": result[1], "max_24hrs": result[2],
                "min_24hrs": result[3], "fiat_volume_24hrs": result[4], "coin_volume_24hrs": result[5]}
        db.child("coinsecure/BTC/INR").push(data)
        add_market_entry('BTC', 'INR', 'Coinsecure', 'coinsecure')
        all_exchange_prices["BTC"]["INR"].append(result[0])
    else:
        print("coinsecure error")

def get_coinsecure_price():
    url = "https://api.coinsecure.in/v1/exchange/ticker"
    r = requests.get(url)
    if r.status_code == 200 or r.status_code == 400: # accepting 400 temporarily because of coinsecure backend error
        json = r.json()
        # does not return 404 if json not found
        if json["success"]:
            try:
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
            except:
                return None

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
        db.child("pocketbits/BTC/INR").push(data)
        add_market_entry('BTC', 'INR', 'PocketBits', 'pocketbits')
        all_exchange_prices["BTC"]["INR"].append(buy_price)
    else:
        print("pockebits error")


def get_pocketbits_price():
    url = "https://www.pocketbits.in/Index/getBalanceRates"

    r = requests.get(url)
    if r.status_code == 200:
        if r.headers["Content-Type"] == "application/json; charset=utf-8":
            json = r.json()
            try:
                buy_price = json["rates"]["BTC_BuyingRate"]
                sell_price = json["rates"]["BTC_SellingRate"]
            except:
                return None

            if buy_price is not None and sell_price is not None:
                return buy_price, sell_price
    return None


###################################################


def update_throughbit_price():
    prices = get_throughbit_price()
    if prices is not None:
        data = {"timestamp": time.time(), "buy_price": prices[0], "sell_price": prices[1]}
        db.child("throughbit/BTC/INR").push(data)
        add_market_entry('BTC', 'INR', 'Throughbit', 'throughbit')
        all_exchange_prices["BTC"]["INR"].append(prices[0])
        data = {"timestamp": time.time(), "buy_price": prices[2], "sell_price": prices[3]}
        db.child("throughbit/ETH/INR").push(data)
        add_market_entry('ETH', 'INR', 'Throughbit', 'throughbit')
        all_exchange_prices["ETH"]["INR"].append(prices[2])

    else:
        print("throughbit error")

def get_throughbit_price():
    url = "https://www.throughbit.com/tbit_ci/index.php/cryptoprice"

    r = requests.get(url)
    if r.status_code == 200:
        json = jsonmodule.loads(r.text)
        try:
            btc_buy_price = json["data"][0]["buy_price"]
            btc_sell_price = json["data"][0]["sell_price"]
            eth_buy_price = json["data"][1]["buy_price"]
            eth_sell_price = json["data"][1]["sell_price"]
        except:
            return None

        if btc_buy_price is not None and btc_sell_price is not None \
                and eth_buy_price is not None and eth_sell_price is not None:
            return [float(btc_buy_price), float(btc_sell_price), float(eth_buy_price), float(eth_sell_price)]
    return None


###################################################

def update_bitbns_price():
    coins = ["BTC", "XRP", "NEO", "GAS", "ETH", "XLM", "RPX", "DBC", "LTC", "XMR", "DASH", "DOGE", "BCH", "SIA", "TRX"]
    result = get_bitbns_price(coins)
    if result is not None:
        for coin in coins:
            data = {"timestamp": time.time(), "buy_price": result[coin]['buy_price'],
                    "sell_price": result[coin]['sell_price']}
            db.child("bitbns/{}/INR".format(coin)).push(data)
            add_market_entry(coin, 'INR', 'Bitbns', 'bitbns')
            all_exchange_prices[coin]["INR"].append(result[coin]['buy_price'])
    else:
        print("bitbns error")

def get_bitbns_price(coins):
    url = "https://bitbns.com/order/getTickerAll"
    data = {}
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        new_dict = dict([(key, d[key]) for d in json for key in d])
        for coin in coins:
            data[coin] = {}
            try:
                data[coin]["buy_price"] = float(new_dict[coin]["buyPrice"])
                data[coin]["sell_price"] = float(new_dict[coin]["sellPrice"])
            except:
                return None

        if data is not None:
            return data
    return None

###################################################


def update_coinome_price():
    coins = ["BTC", "BCH", "LTC", "DASH", "DGB", "ZEC", "QTUM", "BTG"]
    result = get_coinome_price(coins)
    if result is not None:
        for coin in coins:
            data = {"timestamp": time.time(), "buy_price": result[coin]['buy_price'],
                    "sell_price": result[coin]['sell_price']}
            db.child("coinome/{}/INR".format(coin)).push(data)
            add_market_entry(coin, 'INR', 'Coinome', 'coinome')
            all_exchange_prices[coin]["INR"].append(result[coin]['buy_price'])
    else:
        print("coinome error")

def get_coinome_price(coins):
    url = "https://www.coinome.com/api/v1/ticker.json"
    data = {}
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        for coin in coins:
            data[coin] = {}
            trade_pair = "{}-inr".format(coin.lower())
            try:
                data[coin]["buy_price"] = float(json[trade_pair]["lowest_ask"])
                data[coin]["sell_price"] = float(json[trade_pair]["highest_bid"])
            except:
                print("coinome trade pair error for ", trade_pair)
                return None

        if data is not None:
            return data
    return None


###################################################


def update_coindelta_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "OMG", "QTUM"]
    result = get_coindelta_price(coins)
    if result is not None:
        for coin, pair_data in result.items():
            for coin_pair, details in pair_data.items():
                db.child("coindelta").child(coin).child(coin_pair).push(details)
                add_market_entry(coin, coin_pair, 'Coindelta', 'coindelta')
                if coin_pair == "INR":
                    all_exchange_prices[coin]["INR"].append(details["last_price"])
    else:
        print("coindelta error")


def get_coindelta_price(coins):
    data = {}
    for coin in coins:
        data[coin] = {}

    url = "https://coindelta.com/api/v1/public/getticker/"
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        for entry in json:
            try:
                market_name = entry["MarketName"]
                coins = market_name.split('-')
                coin = coins[0].upper()
                base_coin = coins[1].upper()
                data[coin][base_coin] = {}
                data[coin][base_coin]["last_price"] = entry["Last"]
                data[coin][base_coin]["buy_price"]= entry["Ask"]
                data[coin][base_coin]["sell_price"] = entry["Bid"]
            except:
                return None

    if data is not None:
        return data
    return None


###################################################

def update_coinbase_price():
    coins = ["BTC", "ETH", "LTC", "BCH"]
    currencies = ["USD", "GBP", "EUR", "AUD", "SGD", "CAD"]

    for coin in coins:
        for currency in currencies:
            prices = get_coinbase_price(coin, currency)
            stats = get_gdax_market_stats(coin, currency)
            if prices is not None:
                buy_price, sell_price = prices
                if stats is not None:
                    data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price, "max_24hrs": stats[0],
                        "min_24hrs": stats[1], "vol_24hrs": stats[2], "vol_30days": stats[3]}
                else:
                    data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price,
                            "max_24hrs": -1, "min_24hrs": -1, "vol_24hrs": -1, "vol_30days": -1}
                db.child("coinbase/{0}/{1}".format(coin, currency)).push(data)
                add_market_entry(coin, currency, 'Coinbase', 'coinbase')
                all_exchange_prices[coin][currency].append(buy_price)
            else:
                print("coinbase error")


def get_coinbase_price(coin, currency):
    buy_url = "https://api.coinbase.com/v2/prices/{0}-{1}/buy".format(coin, currency)
    sell_url = "https://api.coinbase.com/v2/prices/{0}-{1}/sell".format(coin, currency)

    buy_request = requests.get(buy_url)
    if buy_request.status_code == 200:
        json = buy_request.json()
        try:
            buy_price = json["data"]["amount"]
        except:
            return None

        sell_request = requests.get(sell_url)
        if sell_request.status_code == 200:
            json = sell_request.json()
            try:
                sell_price = json["data"]["amount"]
            except:
                return None

            if buy_price is not None and sell_price is not None:
                return float(buy_price), float(sell_price)
    return None


def get_gdax_market_stats(coin, currency):
    url = "https://api.gdax.com/products/{0}-{1}/stats".format(coin, currency)

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            max_24hrs = json["high"]
            min_24hrs = json["low"]
            vol_24hrs = json["volume"]
            vol_30days = json["volume_30day"]
        except:
            return None

        if max_24hrs is not None and min_24hrs is not None and vol_24hrs is not None and vol_30days is not None:
            return [float(max_24hrs), float(min_24hrs), float(vol_24hrs), float(vol_30days)]

###################################################


def update_kraken_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "DASH", "EOS", "ETC", "GNO", "ICN", "MLN", "REP", "XDG", "XLM", "XMR", "XRP", "ZEC"]
    trade_pairs_dict = {}
    trade_pairs_array = []
    for coin in coins:
        currencies = []
        if coin == "BTC":
            currencies = ["CAD", "EUR", "GBP", "JPY", "USD"]
        elif coin == "ETH":
            currencies = ["CAD", "EUR", "GBP", "JPY", "USD", "BTC"]
        elif coin == "LTC":
            currencies = ["USD", "EUR", "BTC"]
        elif coin == "BCH":
            currencies = ["USD", "EUR", "BTC"]
        elif coin == "DASH":
            currencies = ["USD", "EUR", "BTC"]
        elif coin == "EOS":
            currencies = ["USD", "EUR", "BTC", "ETH"]
        elif coin == "ETC":
            currencies = ["USD", "EUR", "BTC", "ETH"]
        elif coin == "GNO":
            currencies = ["USD", "EUR", "BTC", "ETH"]
        elif coin == "ICN":
            currencies = ["BTC", "ETH"]
        elif coin == "MLN":
            currencies = ["BTC", "ETH"]
        elif coin == "REP":
            currencies = ["USD", "EUR", "BTC", "ETH"]
        elif coin == "XGD":
            currencies = ["BTC"]
        elif coin == "XLM":
            currencies = ["USD", "EUR", "BTC"]
        elif coin == "XMR":
            currencies = ["USD", "EUR", "BTC"]
        elif coin == "XRP":
            currencies = ["CAD", "EUR", "JPY", "USD", "BTC"]
        elif coin == "ZEC":
            currencies = ["EUR", "JPY", "USD", "BTC"]

        trade_pairs_dict[coin] = currencies
        trade_pairs_array.extend(create_trade_pairs_kraken(coin, currencies))

    result = get_kraken_price(trade_pairs_dict, trade_pairs_array)

    for coin, currencies in trade_pairs_dict.items():
        dict_coin = coin
        if coin == "BTC":
            dict_coin = "XBT"
        for currency in currencies:
            dict_currency = currency
            if currency == "BTC":
                dict_currency = "XBT"
            if result is not None:
                data = {"timestamp": time.time(), "buy_price": result[dict_coin][dict_currency]["buy_price"], "sell_price": result[dict_coin][dict_currency]["sell_price"],
                        "vol_24hrs": result[dict_coin][dict_currency]["sell_price"], "max_24hrs": result[dict_coin][dict_currency]["sell_price"], "min_24hrs": result[dict_coin][dict_currency]["sell_price"]}
                db.child("kraken/{0}/{1}".format(coin, currency)).push(data)
                add_market_entry(coin, currency, 'Kraken', 'kraken')
            else:
                print("kraken error")


def get_kraken_price(trade_pairs_dict, trade_pairs_array):
    trade_pairs_string = ",".join(trade_pairs_array)

    url = "https://api.kraken.com/0/public/Ticker?pair={}".format(trade_pairs_string)

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        dict = {}
        for coin, currencies in trade_pairs_dict.items():
            if coin == "BTC":
                coin = "XBT"
            dict[coin] = {}
            for currency in currencies:
                if currency == "BTC":
                    currency = "XBT"

                if coin == "BCH" or coin == "DASH" or coin == "EOS" or coin == "GNO":
                    coin_currency_pair = "{0}{1}".format(coin, currency)
                else:
                    if currency == "XBT" or currency == "ETH":
                        coin_currency_pair = "X{0}X{1}".format(coin, currency)
                    else:
                        coin_currency_pair = "X{0}Z{1}".format(coin, currency)
                try:
                    dict[coin][currency] = {}
                    dict[coin][currency]["buy_price"] = float(json["result"][coin_currency_pair]["a"][0])
                    dict[coin][currency]["sell_price"] = float(json["result"][coin_currency_pair]["b"][0])
                    dict[coin][currency]["vol_24hrs"] = float(json["result"][coin_currency_pair]["v"][1])
                    dict[coin][currency]["max_24hrs"] = float(json["result"][coin_currency_pair]["h"][1])
                    dict[coin][currency]["min_24hrs"] = float(json["result"][coin_currency_pair]["l"][1])
                except:
                    print("error", coin_currency_pair)

        if dict is not None:
            return dict
    return None


def create_trade_pairs_kraken(coin, currencies):
    trade_pairs = []

    for currency in currencies:
        if coin == "BTC":
            trade_pairs.append("XBT{}".format(currency))
        else:
            if currency == "BTC":
                trade_pairs.append("{}XBT".format(coin))
            else:
                trade_pairs.append("{0}{1}".format(coin, currency))

    return trade_pairs

###################################################

def update_poloniex_price():
    prices = get_poloniex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("poloniex_price").push(data)
        all_exchange_prices["BTC"]["USD"].append(buy_price)
    else:
        print("poloniex error")

def get_poloniex_price():
    url = "https://poloniex.com/public?command=returnTicker"
    # workaround - cookie expires on 1st Dec 2018
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
                'cookie': '__cfduid=d8b5b9d7ee920012a5de62f760368aeb31512142306; POLOSESSID=fsfqn9tseg0foclkll5sj14s20; cf_clearance=77cc2cdc7d2dc2ea346c639fb05d6f0e0d76485e-1512195307-1800'}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        json = r.json()
        try:
            buy_price = json["USDT_BTC"]["lowestAsk"]
            sell_price = json["USDT_BTC"]["highestBid"]
        except:
            return None

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

###################################################

def update_gemini_price():
    coins = ["BTC", "ETH"]
    currencies = ["USD", "BTC"]
    for coin in coins:
        for currency in currencies:
            if coin == "BTC" and currency == "BTC":
                continue
            else:
                result = get_gemini_price(coin, currency)
                if result is not None:
                    data = {"timestamp": time.time(), "buy_price": result[0], "sell_price": result[1],
                            "fiat_volume_24hrs": result[2], "coin_volume_24hrs": result[3]}
                    db.child("gemini/{0}/{1}".format(coin, currency)).push(data)
                    add_market_entry(coin, currency, 'Gemini', 'gemini')
                    if currency != "BTC":
                        all_exchange_prices[coin][currency].append(result[0])
                else:
                    print("gemini error")


def get_gemini_price(coin, currency):
    url = "https://api.gemini.com/v1/pubticker/{0}{1}".format(coin, currency)

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            buy_price = json["ask"]
            sell_price = json["bid"]
            fiat_volume_24hrs = json["volume"][currency]
            coin_volume_24hrs = json["volume"][coin]
        except:
            return None

        if buy_price is not None and sell_price is not None and fiat_volume_24hrs is not None \
                and coin_volume_24hrs is not None:
            return float(buy_price), float(sell_price), float(fiat_volume_24hrs), float(coin_volume_24hrs)
    return None

###################################################

def update_bitfinex_price():
    coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "XMR", "OMG", "NEO", "BTG", "GNT",
             "IOT", "BAT", "ZRX", "TRX", "REP", "ETC", "DASH", "QTUM"]

    trade_pairs_dict = {}
    trade_pairs_array = []
    for coin in coins:
        if coin == "BTC":
            currencies = ["USD", "EUR"]
        elif coin == "ETH":
            currencies = ["USD", "BTC"]
        elif coin == "LTC":
            currencies = ["USD", "BTC"]
        elif coin == "BCH":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "XRP":
            currencies = ["USD", "BTC"]
        elif coin == "XMR":
            currencies = ["USD", "BTC"]
        elif coin == "OMG":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "NEO":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "BTG":
            currencies = ["USD", "BTC"]
        elif coin == "GNT":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "IOT":
            currencies = ["USD", "EUR", "BTC", "ETH"]
        elif coin == "BAT":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "ZRX":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "TRX":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "REP":
            currencies = ["USD", "BTC", "ETH"]
        elif coin == "ETC":
            currencies = ["USD", "BTC"]
        elif coin == "DASH":
            currencies = ["USD", "BTC"]
        elif coin == "QTUM":
            currencies = ["USD", "BTC", "ETH"]

        trade_pairs_dict[coin] = currencies
        trade_pairs_array.extend(create_trade_pairs_bitfinex(coin, currencies))

    result = get_bitfinex_price(coins, trade_pairs_dict, trade_pairs_array)

    if result is not None or result != {}:
        for coin, currencies in result.items():
            for currency in currencies:
                data = {"timestamp": time.time(),
                        "buy_price": result[coin][currency]["buy_price"],
                        "sell_price": result[coin][currency]["sell_price"],
                        "max_24hrs": result[coin][currency]["max_24hrs"],
                        "min_24hrs": result[coin][currency]["min_24hrs"],
                        "vol_24hrs": result[coin][currency]["vol_24hrs"]}
                db.child("bitfinex/{0}/{1}".format(coin, currency)).update(data)
                add_market_entry(coin, currency, 'Bitfinex', 'bitfinex')

def get_bitfinex_price(coins, trade_pairs_dict, trade_pairs_array):
    trade_pairs_string = ",".join(trade_pairs_array)
    url = "https://api.bitfinex.com/v2/tickers?symbols={}".format(trade_pairs_string)
    r = requests.get(url)
    if r.status_code == 200:
        if r.headers['Content-Type'] == 'application/json; charset=utf-8':
            json = r.json()
            dict = {}
            index = 0
            for coin in coins:
                dict[coin] = {}
                for currency in trade_pairs_dict[coin]:
                    try:
                        dict[coin][currency] = {}
                        dict[coin][currency]["buy_price"] = float(json[index][3])
                        dict[coin][currency]["sell_price"] = float(json[index][1])
                        dict[coin][currency]["max_24hrs"] = float(json[index][9])
                        dict[coin][currency]["min_24hrs"] = float(json[index][10])
                        dict[coin][currency]["vol_24hrs"] = float(json[index][8])
                    except:
                        print("bitfinex error", coin, currency)

                    index += 1

            if dict is not None:
                return dict
    return None

def create_trade_pairs_bitfinex(coin, currencies):
    trade_pairs = []
    for currency in currencies:
        if coin == "DASH":
            trade_pairs.append("tDSH{}".format(currency))
        elif coin == "QTUM":
            trade_pairs.append("tQTM{}".format(currency))
        else:
            trade_pairs.append("t{0}{1}".format(coin, currency))

    return trade_pairs

###################################################

def update_bitstamp_price():
    coins = ["BTC", "ETH", "LTC", "XRP"]
    currencies = ["USD", "EUR"]
    for coin in coins:
        for currency in currencies:
            result = get_bitstamp_price(coin, currency)
            if result is not None:
                data = {"timestamp": time.time(), "buy_price": result[0], "sell_price": result[1],
                        "max_24hrs": result[2], "min_24hrs": result[3], "vol_24hrs": result[4]}
                db.child("bitstamp/{0}/{1}".format(coin, currency)).push(data)
                db.child("bitstamp_{0}_{1}".format(coin, currency)).remove()
                add_market_entry(coin, currency, 'Bitstamp', 'bitstamp')

                all_exchange_prices[coin][currency].append(result[0])
            else:
                print("bitstamp error")

def get_bitstamp_price(coin, currency):
    url = "https://www.bitstamp.net/api/v2/ticker/{0}{1}".format(coin.lower(), currency.lower())

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            buy_price = json["ask"]
            sell_price = json["bid"]
            max_24hrs = json["high"]
            min_24hrs = json["low"]
            vol_24hrs = json["volume"]
        except:
            return None

        if buy_price is not None and sell_price is not None and max_24hrs is not None \
                and min_24hrs is not None and vol_24hrs is not None:
            return [float(buy_price), float(sell_price), float(max_24hrs), float(min_24hrs), float(vol_24hrs)]
    return None

###################################################

def update_bittrex_price():
    prices = get_bittrex_price()
    if prices is not None:
        buy_price, sell_price = prices
        data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price}
        db.child("bittrex_price").push(data)
        all_exchange_prices["BTC"]["USD"].append(buy_price)
    else:
        print("bittrex error")


def get_bittrex_price():
    url = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            buy_price = json["result"]["Ask"]
            sell_price = json["result"]["Bid"]
        except:
            return None

        if buy_price is not None and sell_price is not None:
            return buy_price, sell_price
    return None

###################################################


def update_kucoin_price():
    result = get_kucoin_price()
    if result is not None:
        for coin, pair_data in result.items():
            for coin_pair, details in pair_data.items():
                db.child("kucoin").child(coin).child(coin_pair).update(details)
                add_market_entry(coin, coin_pair, 'Kucoin', 'kucoin')

    else:
        print("kucoin error")

def get_kucoin_price():
    url = "https://api.kucoin.com/v1/market/open/symbols"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        try:
            status = json["success"]
            if status:
                results = json["data"]
                data = {}

                for result in results:
                    coin = result["coinType"]
                    coin_pair = result["coinTypePair"]

                    if coin not in data:
                        data[coin] = {}

                    data[coin][coin_pair] = {}
                    data[coin][coin_pair]["last_price"] = result["lastDealPrice"]
                    data[coin][coin_pair]["price_change"] = result["change"]
                    data[coin][coin_pair]["percentage_change"] = result["changeRate"] * 100
                    try:
                        data[coin][coin_pair]["high"] = result["high"]
                    except:
                        data[coin][coin_pair]["high"] = result["sell"]

                    try:
                        data[coin][coin_pair]["low"] = result["low"]
                    except:
                        data[coin][coin_pair]["low"] = result["sell"]

                    data[coin][coin_pair]["volume"] = result["volValue"]
                    data[coin][coin_pair]["sell_price"] = result["sell"]
                    try:
                        data[coin][coin_pair]["buy_price"] = result["buy"]
                    except:
                        data[coin][coin_pair]["buy_price"] = result["sell"]

                return data
        except:
            return None
    else:
        return None


###################################################

def update_binance_price():
    result = get_binance_price()


def get_binance_price():
    url = "https://api.binance.com/api/v1/ticker/24hr"

    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        data = {}
        for result in json:
            print(result)


###################################################

def add_market_entry(coin, currency, market_name, market_title):

    if coin not in all_markets :
        all_markets[coin] = {}

    if currency not in all_markets[coin]:
        all_markets[coin][currency] = {}

    all_markets[coin][currency][market_name] = '{0}/{1}/{2}'.format(market_title, coin, currency)


def update_markets():
    for coin, values in all_markets.items():
        for currency, markets in values.items():
            db.child("{0}/Data/{1}/markets".format(coin, currency)).update(markets)

execute()
