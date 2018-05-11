import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from google.cloud.storage import blob

import requests
from itertools import islice
import time
from concurrent.futures import ThreadPoolExecutor
from diskcache import Cache
from diskcache import Index

cred = credentials.Certificate('../service_account_info/Cryptare-9d04b184ba96.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://atalwcryptare.firebaseio.com/',
    'storageBucket': 'atalwcryptare.appspot.com'
})

# As an admin, the app has access to read and write all data, regardless of Security Rules
ref = db.reference()
storageRef = storage.bucket()

cache = Cache('/tmp/coin_alerts_users_marketavg_cache')
cache_store_time = 60*30

icon_cache = Cache('/tmp/icon_cache')
icon_cache_store_time = 60*60*24*7


supported_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                        "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                        "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD",
                        "USD", "ZAR", "BTC", "ETH"]

alert_users = {}

illegal_characters = ["-", "."]


def update_list_of_coins_with_rank():
  temp_multi_path_dict = {}
  cache.expire()
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

          # try:
          #   key = "{}.png".format(symbol.lower())
          #   index = Index.fromcache(cache)
          #   if key in index:
          #     print('in cache - no need to update')
          #   else:
          #     icon = storageRef.get_blob("icons/{}.png".format(symbol.lower()))
          #     icon_url = icon.media_link
          #     # cache.set(key, icon_url, expire=icon_cache_store_time)
          #     print(icon_url)
          #     temp_multi_path_dict['coins/{}/icon_url'.format(symbol)] = icon_url
          # except:
          #   print('url didnt work')
          #   pass

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
      executor.submit(ref.update(item))

def dict_chunks(data, SIZE=500):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k: data[k] for k in islice(it, SIZE)}


def get_market_average_alerts_users():
  cache.expire()

  key = 'coin_alerts_users/MarketAverage'
  index = Index.fromcache(cache)
  if key in index:
    # print('in cache')
    return dict(index[key])
  else:
    data = ref.child(key).get()
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