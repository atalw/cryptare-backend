# -*- coding: utf-8 -*-
# !/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import requests
import pyrebase
import time
import json as jsonmodule
from binance.client import Client
import ccxt
from itertools import islice

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
         "SIA", "TRX", "DGB", "ZEC", "BTG", "IOT", "ZIL", "ETN", "ONT", "KNC",
         "EOS", "POLY", "AION", "NCASH", "ICX", "VEN"]

currencies = ["INR", "USD", "GBP", "CAD", "JPY", "CNY", "SGD", "EUR", "ZAR", "AUD"]

all_markets = {}
all_exchange_update_type = {}

all_exchange_prices = {}
all_market_data = {}


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


def update_average_price():
  for coin, currency_data in all_exchange_prices.items():
    for currency, exchange_data in currency_data.items():
      count = len(exchange_data)
      if count > 0:
        total_sum = 0
        for key, value in exchange_data.items():
          total_sum = total_sum + value
        average = total_sum / count

        all_market_data['{0}/Data/{1}/price'.format(coin, currency)] = average


###################################################


def update_zebpay_price():
  coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "EOS", "OMG"]
  result = get_zebpay_price(coins)
  if result is not None:
    for coin in coins:
      data = {"timestamp": time.time(), "last_price": result[coin]["last_price"],
              "buy_price": result[coin]["buy_price"],
              "sell_price": result[coin]["sell_price"], "vol_24hrs": result[coin]["vol_24hrs"]}
      all_market_data["zebpay/{}/INR".format(coin)] = data
      add_market_price(coin, 'INR', 'Zebpay', result[coin]["buy_price"])
      add_market_entry(coin, 'INR', 'Zebpay', 'zebpay')
    all_exchange_update_type['Zebpay'] = 'update'
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
        data[coin]["last_price"] = float(json["market"])
        data[coin]["buy_price"] = float(json["buy"])
        data[coin]["sell_price"] = float(json["sell"])
        data[coin]["vol_24hrs"] = float(json["volume"])
      except:
        return None
    else:
      return None

  if data is not None:
    return data
  return None


###################################################


def update_koinex_price():
  # make only 1 API call to koinex
  result = get_koinex_price()
  if result is not None:
    for coin, quote_coins in result.items():
      for quote, values in quote_coins.items():
        all_market_data["koinex/{0}/{1}".format(coin, quote)] = values
        add_market_entry(coin, quote, 'Koinex', 'koinex')
        if quote == 'INR':
          add_market_price(coin, quote, 'Koinex', values["buy_price"])
    all_exchange_update_type['Koinex'] = 'update'
  else:
    print("koinex error")


def get_koinex_price():
  url = "https://koinex.in/api/ticker"
  data = {}
  r = requests.get(url)
  if r.status_code == 200:
    json = r.json()

    for key, result in json.items():
      if key == "stats":
        try:
          for quote, all_coins in result.items():
            if quote == "inr":
              pair = "INR"
            elif quote == "bitcoin":
              pair = "BTC"
            elif quote == "ether":
              pair = "ETH"

            for coin, entry in all_coins.items():

              if coin not in data:
                data[coin] = {}

              if pair not in data[coin]:
                data[coin][pair] = {}

              last_traded_price = entry["last_traded_price"]
              lowest_ask = entry["lowest_ask"]
              highest_bid = entry["highest_bid"]
              vol_24hrs = entry["vol_24hrs"]
              max_24hrs = entry["max_24hrs"]
              min_24hrs = entry["min_24hrs"]
              per_change = entry["per_change"]

              data[coin][pair]['last_price'] = string_to_float(last_traded_price)
              data[coin][pair]['buy_price'] = string_to_float(lowest_ask)
              data[coin][pair]['sell_price'] = string_to_float(highest_bid)
              data[coin][pair]['vol_24hrs'] = string_to_float(vol_24hrs)
              data[coin][pair]['max_24hrs'] = string_to_float(max_24hrs)
              data[coin][pair]['min_24hrs'] = string_to_float(min_24hrs)
              data[coin][pair]['per_change_24hrs'] = string_to_float(per_change)
              data[coin][pair]['timestamp'] = time.time()

        except:
          return None

    if data is not None:
      return data
  return None


def string_to_float(value):
  if value is not None:
    return float(value)
  else:
    return 0

###################################################


def update_localbitcoins_price():
  # JPY currency not available
  currencies = ["INR", "USD", "GBP", "CNY", "SGD", "EUR", "ZAR"]

  volume_data = get_localbitcoins_volume(currencies)
  for currency in currencies:
    prices = get_localbitcoins_price(currency)
    if prices is not None and volume_data is not None:
      buy_price, sell_price = prices
      data = {"timestamp": time.time(), "buy_price": buy_price, "sell_price": sell_price,
              "vol_24hrs": volume_data[currency]}
      title = "localbitcoins/BTC/{}".format(currency)
      all_market_data[title] = data
      add_market_entry('BTC', currency, 'Localbitcoins', 'localbitcoins')
      add_market_price('BTC', currency, 'Localbitcoins', buy_price)
      all_exchange_update_type['Localbitcoins'] = 'update'
    else:
      print("localbitcoins error")
      return


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
    # db.child("coinsecure/BTC/INR").update(data)
    add_market_entry('BTC', 'INR', 'Coinsecure', 'coinsecure')
    add_market_price('BTC', 'INR', 'Coinsecure', result[0])
    all_exchange_update_type['Coinsecure'] = 'update'
  else:
    print("coinsecure error")


def get_coinsecure_price():
  url = "https://api.coinsecure.in/v1/exchange/ticker"
  r = requests.get(url)
  if r.status_code == 200 or r.status_code == 400:  # accepting 400 temporarily because of coinsecure backend error
    json = r.json()
    # does not return 404 if json not found
    if json["success"]:
      try:
        buy_price_in_paisa = json["message"]["ask"]
        buy_price = buy_price_in_paisa / 100

        sell_price_in_paisa = json["message"]["bid"]
        sell_price = sell_price_in_paisa / 100

        max_24hrs_in_paisa = json["message"]["high"]
        max_24hrs = max_24hrs_in_paisa / 100

        min_24hrs_in_paisa = json["message"]["low"]
        min_24hrs = min_24hrs_in_paisa / 100

        fiat_volume_in_paisa = json["message"]["fiatvolume"]
        fiat_volume_24hrs = fiat_volume_in_paisa / 100

        coin_volume = json["message"]["coinvolume"]
        coin_volume_24hrs = coin_volume / 100000000
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
    all_market_data["pocketbits/BTC/INR"] = data
    add_market_entry('BTC', 'INR', 'PocketBits', 'pocketbits')
    add_market_price('BTC', 'INR', 'PocketBits', buy_price)
    all_exchange_update_type['PocketBits'] = 'update'
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
    all_market_data["throughbit/BTC/INR"] = data
    add_market_entry('BTC', 'INR', 'Throughbit', 'throughbit')
    add_market_price('BTC', 'INR', 'Throughbit', prices[0])

    data = {"timestamp": time.time(), "buy_price": prices[2], "sell_price": prices[3]}
    all_market_data["throughbit/ETH/INR"] = data
    add_market_entry('ETH', 'INR', 'Throughbit', 'throughbit')
    add_market_price('ETH', 'INR', 'Throughtbit', prices[2])
    all_exchange_update_type['Throughbit'] = 'update'
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
  result = get_bitbns_price()
  if result is not None:
    all_exchange_update_type['Bitbns'] = 'update'
    for coin, value in result.items():
      data = {"timestamp": time.time(), "buy_price": value['buy_price'],
              "sell_price": value['sell_price']}
      all_market_data["bitbns/{}/INR".format(coin)] = data
      add_market_entry(coin, 'INR', 'Bitbns', 'bitbns')
      add_market_price(coin, 'INR', 'Bitbns', value['buy_price'])
  else:
    print("bitbns error")


def get_bitbns_price():
  url = "https://bitbns.com/order/getTickerAll"
  data = {}
  r = requests.get(url)
  if r.status_code == 200:
    json = r.json()
    new_dict = dict([(key, d[key]) for d in json for key in d])
    for coin in new_dict:
      if coin not in coins:
        coins.append(coin)
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
      all_market_data["coinome/{}/INR".format(coin)] = data
      add_market_entry(coin, 'INR', 'Coinome', 'coinome')
      add_market_price(coin, 'INR', 'Coinome', result[coin]['buy_price'])
    all_exchange_update_type['Coinome'] = 'update'
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
  result = get_coindelta_price()
  if result is not None:
    for coin, pair_data in result.items():
      for coin_pair, details in pair_data.items():
        all_market_data['coindelta/{0}/{1}'.format(coin, coin_pair)] = details
        add_market_entry(coin, coin_pair, 'Coindelta', 'coindelta')
        if coin_pair == "INR":
          add_market_price(coin, 'INR', 'Coindelta', details['last_price'])
    all_exchange_update_type['Coindelta'] = 'update'
  else:
    print("coindelta error")


def get_coindelta_price():
  data = {}

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

        if coin not in data:
          data[coin] = {}

        data[coin][base_coin] = {}
        data[coin][base_coin]["last_price"] = entry["Last"]
        data[coin][base_coin]["buy_price"] = entry["Ask"]
        data[coin][base_coin]["sell_price"] = entry["Bid"]
      except:
        return None
  else:
    return None
  if data is not None:
    return data
  return None


###################################################

def update_wazirx_price():
  result = get_wazirx_price()

  if result is not None:
    for coin, pair_data in result.items():
      for coin_pair, details in pair_data.items():
        all_market_data['wazirx/{0}/{1}'.format(coin, coin_pair)] = details
        add_market_entry(coin, coin_pair, 'WazirX', 'wazirx')
        if coin_pair == "INR":
          add_market_price(coin, coin_pair, 'WazirX', details['last_price'])
    all_exchange_update_type['WazirX'] = 'update'
  else:
    print("wazirx error")


def get_wazirx_price():
  data = {}
  url = "https://api.wazirx.com/api/v2/tickers"
  r = requests.get(url)
  if r.status_code == 200:
    json = r.json()
    for key, entry in json.items():
      try:
        base = entry["base_unit"].upper()
        quote = entry["quote_unit"].upper()
        if base not in data:
          data[base] = {}

        data[base][quote] = {}
        data[base][quote]["buy_price"] = float(entry["buy"])
        data[base][quote]["sell_price"] = float(entry["sell"])
        data[base][quote]["last_price"] = float(entry["last"])
        data[base][quote]["max_24hrs"] = float(entry["high"])
        data[base][quote]["min_24hrs"] = float(entry["low"])
        data[base][quote]["vol_24hrs"] = float(entry["volume"])
        data[base][quote]["timestamp"] = float(entry["at"])
      except:
        return None
  else:
    return None

  if data is not None:
    return data
  return None


###################################################

def update_coindcx_price():
  result = get_coindcx_price()

  if result is not None:
    for coin, pair_data in result.items():
      for coin_pair, details in pair_data.items():
        all_market_data['coindcx/{0}/{1}'.format(coin, coin_pair)] = details
        add_market_entry(coin, coin_pair, 'CoinDCX', 'coindcx')
        if coin_pair == "INR":
          add_market_price(coin, coin_pair, 'CoinDCX', details['last_price'])
    all_exchange_update_type['CoinDCX'] = 'update'
  else:
    print("coindcx error")


def get_coindcx_price():
  data = {}
  currency_pairs_url = "https://api.coindcx.com/api/v1/app_data"
  price_url = "https://api.coindcx.com/api/v1/trending_pairs/"

  r = requests.get(currency_pairs_url)
  if r.status_code == 200:
    json = r.json()
    for entry in json['currency_pairs']:
      try:
        base = entry["base_currency_short_name"]
        quote = entry["target_currency_short_name"]
        if quote not in data:
          data[quote] = {}

        if quote not in coins:
          coins.append(quote)

        data[quote][base] = {}
      except:
        return None

    r = requests.get(price_url)
    if r.status_code == 200:
      json = r.json()
      try:
        all_current_prices = json['currenct_prices']
        for quote, base_array in data.items():
          for base in base_array:
            price = float(all_current_prices['{0}{1}'.format(quote, base)])
            data[quote][base]['buy_price'] = price
            data[quote][base]['sell_price'] = price
      except:
        return None
  else:
    return None

  if data is not None:
    return data
  return None


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
        all_market_data["coinbase/{0}/{1}".format(coin, currency)] = data
        add_market_entry(coin, currency, 'Coinbase', 'coinbase')
        # add_market_price(coin, currency, 'Coinbase', buy_price)
        all_exchange_update_type['Coinbase'] = 'update'
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
  coins = ["BTC", "ETH", "LTC", "BCH", "DASH", "EOS", "ETC", "GNO", "ICN", "MLN", "REP", "XDG", "XLM", "XMR", "XRP",
           "ZEC"]
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
        data = {"timestamp": time.time(), "buy_price": result[dict_coin][dict_currency]["buy_price"],
                "sell_price": result[dict_coin][dict_currency]["sell_price"],
                "vol_24hrs": result[dict_coin][dict_currency]["sell_price"],
                "max_24hrs": result[dict_coin][dict_currency]["sell_price"],
                "min_24hrs": result[dict_coin][dict_currency]["sell_price"]}
        all_market_data["kraken/{0}/{1}".format(coin, currency)] = data
        add_market_entry(coin, currency, 'Kraken', 'kraken')
        all_exchange_update_type['Kraken'] = 'update'
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
    # all_exchange_prices["BTC"]["USD"].append(buy_price)
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
          all_market_data["gemini/{0}/{1}".format(coin, currency)] = data
          add_market_entry(coin, currency, 'Gemini', 'gemini')
          # if currency != "BTC":
          # all_exchange_prices[coin][currency].append(result[0])
          all_exchange_update_type['Gemini'] = 'update'
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
        all_market_data["bitfinex/{0}/{1}".format(coin, currency)] = data
        add_market_entry(coin, currency, 'Bitfinex', 'bitfinex')
    all_exchange_update_type['Bitfinex'] = 'update'


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
        all_market_data["bitstamp/{0}/{1}".format(coin, currency)] = data
        add_market_entry(coin, currency, 'Bitstamp', 'bitstamp')

        # all_exchange_prices[coin][currency].append(result[0])
        all_exchange_update_type['Bitstamp'] = 'update'
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
    all_market_data["bittrex"] = data
    # all_exchange_prices["BTC"]["USD"].append(buy_price)
    all_exchange_update_type['Bittrex'] = 'update'
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
        all_market_data["kucoin/{0}/{1}".format(coin, coin_pair)] = details
        add_market_entry(coin, coin_pair, 'Kucoin', 'kucoin')
    all_exchange_update_type['Kucoin'] = 'update'

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
  client = Client("", "")
  dict = {}

  info = client.get_exchange_info()

  for entry in info['symbols']:
    if entry['status'] == 'TRADING':
      coin = entry['baseAsset']
      coin_pair = entry['quoteAsset']
      if coin not in dict:
        dict[coin] = {}

      if coin_pair not in dict[coin]:
        dict[coin][coin_pair] = {}

  tickers = client.get_ticker()

  for entry in tickers:
    for coin, coin_pairs in dict.items():
      for coin_pair in coin_pairs:
        if entry['symbol'] == '{0}{1}'.format(coin, coin_pair):
          dict[coin][coin_pair]['buy_price'] = float(entry['askPrice'])
          dict[coin][coin_pair]['sell_price'] = float(entry['bidPrice'])
          dict[coin][coin_pair]['max_24hrs'] = float(entry['highPrice'])
          dict[coin][coin_pair]['min_24hrs'] = float(entry['lowPrice'])
          dict[coin][coin_pair]['vol_24hrs'] = float(entry['volume'])

  for coin, coin_pairs in dict.items():
    for coin_pair in coin_pairs:
      all_market_data['binance/{0}/{1}'.format(coin, coin_pair)] = dict[coin][coin_pair]
      add_market_entry(coin, coin_pair, 'Binance', 'binance')
  all_exchange_update_type['Binance'] = 'update'


###################################################


def update_huobi_price():
  result = get_huobi_price()
  if result is not None:
    for coin, coin_pairs in result.items():
      for coin_pair in coin_pairs:
        all_market_data['huobi/{0}/{1}'.format(coin.upper(), coin_pair.upper())] = result[coin][coin_pair]
        add_market_entry(coin.upper(), coin_pair.upper(), 'Huobi', 'huobi')
    all_exchange_update_type['Huobi'] = 'update'
  else:
    print('huobi error')


def get_huobi_price():
  symbols_dict = get_huobi_symbols()
  if symbols_dict is not None:
    for coin, coin_pairs in symbols_dict.items():
      for coin_pair in coin_pairs:
        url = "https://api.huobi.pro/market/detail/merged?symbol={0}{1}".format(coin, coin_pair)

        r = requests.get(url)
        if r.status_code == 200:
          json = r.json()
          try:
            if json['status'] == 'ok':
              timestamp = json['ts']
              symbols_dict[coin][coin_pair]['buy_price'] = float(json['tick']['ask'][0])
              symbols_dict[coin][coin_pair]['sell_price'] = float(json['tick']['bid'][0])
              symbols_dict[coin][coin_pair]['max_24hrs'] = float(json['tick']['high'])
              symbols_dict[coin][coin_pair]['min_24hrs'] = float(json['tick']['low'])
              symbols_dict[coin][coin_pair]['vol_24hrs'] = float(json['tick']['vol'])
              symbols_dict[coin][coin_pair]['timestamp'] = timestamp
          except:
            print(coin, coin_pair, 'huobi error')
    return symbols_dict
  else:
    return None


def get_huobi_symbols():
  url = "https://api.huobi.pro/v1/common/symbols"

  r = requests.get(url)
  if r.status_code == 200:
    json = r.json()
    try:
      if json['status'] == 'ok':
        symbols_dict = {}
        for entry in json['data']:
          coin = entry['base-currency']
          coin_pair = entry['quote-currency']
          if coin not in symbols_dict:
            symbols_dict[coin] = {}
          if coin_pair not in symbols_dict[coin]:
            symbols_dict[coin][coin_pair] = {}
        return symbols_dict
    except:
      print('huobi symbol error')
      return None
  return None


###################################################


def update_hitbtc_price():
  hitbtc = ccxt.hitbtc()
  hitbtc_markets = hitbtc.fetch_markets()
  hitbtc_tickers = hitbtc.fetch_tickers()

  dict = {}

  for symbol in hitbtc_markets:
    coin = symbol['base']
    coin_pair = symbol['quote']
    if coin not in dict:
      dict[coin] = {}
    if coin_pair not in dict[coin]:
      dict[coin][coin_pair] = {}

  for coin, coin_pairs in dict.items():
    for coin_pair in coin_pairs:
      symbol = "{0}/{1}".format(coin, coin_pair)
      info = hitbtc_tickers[symbol]
      try:
        dict[coin][coin_pair]['buy_price'] = float(info['ask'])
        dict[coin][coin_pair]['sell_price'] = float(info['bid'])
        dict[coin][coin_pair]['last_price'] = float(info['last'])
        dict[coin][coin_pair]['max_24hrs'] = float(info['high'])
        dict[coin][coin_pair]['min_24hrs'] = float(info['low'])
        dict[coin][coin_pair]['vol_24hrs'] = float(info['baseVolume'])
      except:
        continue

  for coin, coin_pairs in dict.items():
    for coin_pair in coin_pairs:
      all_market_data['hitbtc/{0}/{1}'.format(coin, coin_pair)] = dict[coin][coin_pair]
      add_market_entry(coin, coin_pair, 'HitBTC', 'hitbtc')
  all_exchange_update_type['HitBTC'] = 'update'


###################################################


def update_ccxt_market_price(market, market_name, market_database_title):
  market_markets = market.fetch_markets()
  market_tickers = market.fetch_tickers()

  dict = {}

  for symbol in market_markets:
    coin = symbol['base']
    coin_pair = symbol['quote']
    if coin not in dict:
      dict[coin] = {}
    if coin_pair not in dict[coin]:
      dict[coin][coin_pair] = {}

  for coin, coin_pairs in dict.items():
    for coin_pair in coin_pairs:
      symbol = "{0}/{1}".format(coin, coin_pair)
      info = market_tickers[symbol]
      try:
        dict[coin][coin_pair]['buy_price'] = float(info['ask'])
        dict[coin][coin_pair]['sell_price'] = float(info['bid'])
        dict[coin][coin_pair]['last_price'] = float(info['last'])
        dict[coin][coin_pair]['max_24hrs'] = float(info['high'])
        dict[coin][coin_pair]['min_24hrs'] = float(info['low'])
        dict[coin][coin_pair]['vol_24hrs'] = float(info['baseVolume'])
      except:
        continue

  for coin, coin_pairs in dict.items():
    for coin_pair in coin_pairs:
      all_market_data["{0}/{1}/{2}".format(market_database_title, coin, coin_pair)] = dict[coin][coin_pair]
      add_market_entry(coin, coin_pair, '{}'.format(market_name), '{}'.format(market_database_title))
  all_exchange_update_type['{}'.format(market_name)] = 'update'


###################################################


def add_market_price(coin, currency, market_name, price):
  if coin not in all_exchange_prices:
    all_exchange_prices[coin] = {}

  if currency not in all_exchange_prices[coin]:
    all_exchange_prices[coin][currency] = {}

  all_exchange_prices[coin][currency][market_name] = price


def add_market_entry(coin, currency, market_name, market_title):
  if coin not in all_markets:
    all_markets[coin] = {}

  if currency not in all_markets[coin]:
    all_markets[coin][currency] = {}

  if market_name == "Quoinex" and currency == "INR":
    pass
  else:
    all_markets[coin][currency][market_name] = '{0}/{1}/{2}'.format(market_title, coin, currency)


def update_markets():
  for coin, values in all_markets.items():
    for currency, markets in values.items():
      title = "{0}/Data/{1}/markets".format(coin, currency)
      if (currency == "USDT" or currency == "USD") and coin == "BTC":
        usd_title = "{}/Data/USD/markets".format(coin)
        if usd_title not in all_market_data:
          all_market_data[usd_title] = {}
        all_market_data[usd_title].update(markets)
      else:
        all_market_data[title] = markets


def update_exchange_update_type():
  """Store type of update method used for exchange data in Firebase - 'push' or 'update' """
  db.child("all_exchanges_update_type").update(all_exchange_update_type)


def update_all_market_data():
  for item in dict_chunks(all_market_data, 500):
    db.update(item)


def dict_chunks(data, SIZE=10000):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k: data[k] for k in islice(it, SIZE)}


###################################################

with ThreadPoolExecutor() as executor:
  # Indian exchanges
  executor.submit(update_zebpay_price)
  executor.submit(update_localbitcoins_price)
  executor.submit(update_pocketbits_price)
  # executor.submit(update_coinsecure_price)
  executor.submit(update_wazirx_price)
  executor.submit(update_koinex_price)
  executor.submit(update_bitbns_price)
  executor.submit(update_coinome_price)
  executor.submit(update_coindelta_price)
  executor.submit(update_throughbit_price)
  executor.submit(update_coindcx_price)

  # US exchanges
  executor.submit(update_coinbase_price)
  executor.submit(update_kraken_price)
  executor.submit(update_gemini_price)
  executor.submit(update_bitfinex_price)
  executor.submit(update_bitstamp_price)
  # executor.submit(update_poloniex_price)
  # executor.submit(update_bittrex_price)

  executor.submit(update_kucoin_price)
  executor.submit(update_binance_price)
  executor.submit(update_hitbtc_price)
  # executor.submit(update_huobi_price) # very very slow

  executor.submit(update_ccxt_market_price, ccxt.gateio(), 'GateIO', 'gateio')
  executor.submit(update_ccxt_market_price, ccxt.cex(), 'CexIO', 'cexio')
  executor.submit(update_ccxt_market_price, ccxt.quoinex(), 'Quoinex', 'quoinex')
  executor.submit(update_ccxt_market_price, ccxt.lakebtc(), 'LakeBTC', 'lakebtc')
  executor.submit(update_ccxt_market_price, ccxt.bittrex(), 'Bittrex', 'bittrex')

  executor.submit(update_ccxt_market_price, ccxt.bithumb(), 'Bithumb', 'bithumb')
  executor.submit(update_ccxt_market_price, ccxt.luno(), 'Luno', 'luno')
  executor.submit(update_ccxt_market_price, ccxt.exmo(), 'EXMO', 'exmo')
  executor.submit(update_ccxt_market_price, ccxt.dsx(), 'DSX', 'dsx')
  # executor.submit(update_ccxt_market_price, ccxt.cryptopia(), 'Cryptopia', 'cryptopia') # key error
  executor.submit(update_ccxt_market_price, ccxt.wex(), 'WEX', 'wex')
  executor.submit(update_ccxt_market_price, ccxt.therock(), 'TheRockTrading', 'therock')
  executor.submit(update_ccxt_market_price, ccxt.southxchange(), 'SouthXchange', 'southxchange')
  executor.submit(update_ccxt_market_price, ccxt.qryptos(), 'QRYPTOS', 'qryptos')
  executor.submit(update_ccxt_market_price, ccxt.livecoin(), 'LiveCoin', 'livecoin')
  executor.submit(update_ccxt_market_price, ccxt.liqui(), 'Liqui', 'liqui')
  executor.submit(update_ccxt_market_price, ccxt.kuna(), 'Kuna', 'kuna')
  executor.submit(update_ccxt_market_price, ccxt.cobinhood(), 'COBINHOOD', 'cobinhood')
  executor.submit(update_ccxt_market_price, ccxt.btctradeim(), 'BtcTradeIM', 'btctradeim')
  executor.submit(update_ccxt_market_price, ccxt.braziliex(), 'Braziliex', 'braziliex')
  executor.submit(update_ccxt_market_price, ccxt.bittrex(), 'Bittrex', 'bittrex')
  executor.submit(update_ccxt_market_price, ccxt.acx(), 'ACX', 'acx')


  # executor.submit(update_ccxt_market_price, ccxt.coinegg(), 'CoinEgg', 'coinegg')
  # executor.submit(update_ccxt_market_price, ccxt.tidex(), 'Tidex', 'tidex')


# print(ccxt.exchanges)
update_average_price()
update_markets()
update_exchange_update_type()
update_all_market_data()


# update_ccxt_market_price(ccxt.coinfloor(), 'Coinfloor', 'coinfloor')
# update_ccxt_market_price(ccxt.bitflyer(), 'Bitflyer', 'bitflyer')
# update_ccxt_market_price(ccxt.yobit(), 'YoBit', 'yobit')
# update_ccxt_market_price(ccxt.bitbay(), 'BitBay', 'bitbay')
