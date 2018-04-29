import requests
import pyrebase
from itertools import islice
import time
from concurrent.futures import ThreadPoolExecutor
from diskcache import Cache
from diskcache import Index

config = {
  "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
  "authDomain": "atalwcryptare.firebaseapp.com",
  "databaseURL": "https://atalwcryptare.firebaseio.com/",
  "storageBucket": "atalwcryptare.appspot.com",
  "serviceAccount": "../service_account_info/Cryptare-9d04b184ba96.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
storage = firebase.storage()

cache = Cache('/tmp/coin_alerts_users_marketavg_cache')
cache_store_time = 60*30

supported_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                        "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                        "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD",
                        "USD", "ZAR"]

alert_users = {}

illegal_characters = ["-", "."]


def update_list_of_coins_with_rank():
  temp_multi_path_dict = {}

  for currency in supported_currencies:
    url = "https://api.coinmarketcap.com/v1/ticker/?convert={}&limit=300".format(currency)

    r = requests.get(url)
    if r.status_code == 200:
      json = r.json()

      for coin in json:
        symbol = coin["symbol"]
        if symbol == "MIOTA":
          symbol = "IOT"
        elif symbol == "NANO":
          symbol = "XRB"

        if is_symbol_valid(symbol):
          if not any(substring in symbol for substring in illegal_characters) and not any(
                  substring in coin["name"] for substring in illegal_characters):
            temp_multi_path_dict['coins/{}/rank'.format(symbol)] = string_to_float(coin["rank"])
            temp_multi_path_dict['coins/{}/name'.format(symbol)] = coin["name"]
          else:
            continue

          try:
            icon_url = storage.child("icons/{}.png".format(symbol.lower())).get_url(token=None)
            temp_multi_path_dict['coins/{}/icon_url'.format(symbol)] = icon_url
          except:
            pass

          lower_currency = currency.lower()
          price = string_to_float(coin['price_{}'.format(lower_currency)])
          temp_multi_path_dict['{0}/Data/{1}/price'.format(symbol, currency)] = price
          temp_multi_path_dict['{0}/Data/{1}/vol_24hrs_fiat'.format(symbol, currency)] = string_to_float(
            coin['24h_volume_{}'.format(lower_currency)])
          temp_multi_path_dict['{0}/Data/{1}/supply'.format(symbol, currency)] = string_to_float(coin['available_supply'])
          temp_multi_path_dict['{0}/Data/{1}/marketcap'.format(symbol, currency)] = string_to_float(
            coin['market_cap_{}'.format(lower_currency)])
          temp_multi_path_dict['{0}/Data/{1}/change_24hrs_percent'.format(symbol, currency)] = string_to_float(
            coin['percent_change_24h'])
          temp_multi_path_dict['{0}/Data/{1}/timestamp'.format(symbol, currency)] = time.time()

          # coin alerts users for MarketAverage
          if symbol in alert_users:
            if currency in alert_users[symbol]:
              users = alert_users[symbol][currency]
              for user, count in users.items():
                for index in range(count):
                  title = 'coin_alerts/{0}/MarketAverage/{1}/{2}/{3}/current_price'.format(user, symbol, currency, index)
                  temp_multi_path_dict[title] = price

    else:
      return "list coin error"


  with ThreadPoolExecutor() as executor:
    for item in dict_chunks(temp_multi_path_dict, 500):
      executor.submit(db.update(item))

def dict_chunks(data, SIZE=500):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k: data[k] for k in islice(it, SIZE)}


def get_market_average_alerts_users():
  cache.expire()

  key = 'coin_alerts_users/MarketAverage'
  index = Index.fromcache(cache)
  if key in index:
    print('in cache')
    return dict(index[key])
  else:
    print('not in cache')
    data = db.child(key).get().val()
    if data is not None:
      cache.set(key, data, expire=cache_store_time)
      return dict(data)
    else:
      cache.set(key, {}, expire=cache_store_time)
      return {}


def string_to_float(value):
  if value is not None:
    return float(value)
  else:
    return 0


def is_symbol_valid(symbol):
  if '.' not in symbol and '$' not in symbol  \
    and '[' not in symbol and ']' not in symbol \
    and '#' not in symbol and '/' not in symbol:
    return True
  else:
    return False

alert_users = get_market_average_alerts_users()
update_list_of_coins_with_rank()