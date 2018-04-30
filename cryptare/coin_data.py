import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
import time
from itertools import islice
from diskcache import Cache
from diskcache import Index

cred = credentials.Certificate('../service_account_info/Cryptare-9d04b184ba96.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://atalwcryptare.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regardless of Security Rules
ref = db.reference()

cache = Cache('/tmp/list_of_coins_cache')
cache_store_time = 60*60*12

# coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR", "BTC", "ETH", "CAD", "AUD", "TRY", "AED"]

all_data = {}
multi_path_dict = {}


def get_current_crypto_price():
  crypto_dict = get_list_of_coins_with_rank()
  if crypto_dict is not None:
    crypto_list = list()
    for i in crypto_dict.keys():
      crypto_list.append(i)

    crypto_list_string = list()

    if len(crypto_list) > 60:
      crypto_list_chunks = list(chunks(crypto_list, 50))
      for index, value in enumerate(crypto_list_chunks):
        crypto_list_string.append(",".join(value))
    else:
      crypto_list_string.append(",".join(crypto_list))

    currency_list_string = ",".join(currencies)

    exchange_rate_url = "https://api.fixer.io/latest?symbols=INR&base=USD"
    r = requests.get(exchange_rate_url)
    if r.status_code == 200:
      exchange_json = r.json()
      rate = exchange_json["rates"]["INR"]

    for index, value in enumerate(crypto_list_string):
      url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(value,
                                                                                             currency_list_string)
      r = requests.get(url)
      if r.status_code == 200:
        json = r.json()
        data = json["RAW"]
        for crypto in crypto_list:
          for currency in currencies:
            if crypto in data and currency in data[crypto]:

              multi_path_dict['{0}/Data/{1}/timestamp'.format(crypto, currency)] = time.time()

              if currency == "INR" and rate is not None:
                multi_path_dict['{0}/Data/{1}/change_24hrs_fiat'.format(crypto, currency)] = float(
                  data[crypto]["USD"]["CHANGE24HOUR"] * rate)
              else:
                multi_path_dict['{0}/Data/{1}/change_24hrs_fiat'.format(crypto, currency)] = float(
                  data[crypto][currency]["CHANGE24HOUR"])

              multi_path_dict['{0}/Data/{1}/vol_24hrs_coin'.format(crypto, currency)] = float(
                data[crypto][currency]["VOLUME24HOUR"])
              multi_path_dict['{0}/Data/{1}/high_24hrs'.format(crypto, currency)] = float(
                data[crypto][currency]["HIGH24HOUR"])
              multi_path_dict['{0}/Data/{1}/low_24hrs'.format(crypto, currency)] = float(
                data[crypto][currency]["LOW24HOUR"])
              multi_path_dict['{0}/Data/{1}/last_trade_volume'.format(crypto, currency)] = float(
                data[crypto][currency]["LASTVOLUME"])
              multi_path_dict['{0}/Data/{1}/last_trade_market'.format(crypto, currency)] = data[crypto][currency][
                "LASTMARKET"]

    for item in dict_chunks(multi_path_dict, 500):
      ref.update(item)


def get_list_of_coins_with_rank():
  cache.expire()
  key = 'coins'
  index = Index.fromcache(cache)

  if key in index:
    print('in cache')
    return dict(index[key])
  else:
    all_data = ref.child("coins").get()
    cache.set(key, all_data, expire=cache_store_time)
    return dict(all_data)


def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in range(0, len(l), n):
    yield l[i:i + n]


def dict_chunks(data, SIZE=500):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k: data[k] for k in islice(it, SIZE)}


get_current_crypto_price()