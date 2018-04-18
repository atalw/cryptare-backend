import requests
import pyrebase
import time
import json
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

# coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR", "BTC", "ETH", "CAD", "AUD", "TRY", "AED"]

crypto_with_markets_list = ["BTC", "BCH", "ETH", "XRP", "LTC", "OMG", "REQ", "ZRX", "GNT", "BAT",
                            "AE", "RPX", "DBC", "XMR", "DOGE", "SIA", "XLM", "NEO", "TRX", "DGB",
                            "ZEC", "QTUM", "GAS", "DASH", "BTG", "IOT", "ZIL", "ETN", "ONT", "KNC",
                            "EOS", "POLY", "AION", "NCASH", "ICX", "VEN"]

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

              # if currency == "INR" and crypto in crypto_with_markets_list:
              #     pass
              # else:
              #     multi_path_dict['{0}/Data/{1}/price'.format(crypto, currency)] = float(
              #         data[crypto][currency]["PRICE"])

              multi_path_dict['{0}/Data/{1}/timestamp'.format(crypto, currency)] = time.time()

              if currency == "INR" and rate is not None:
                multi_path_dict['{0}/Data/{1}/change_24hrs_fiat'.format(crypto, currency)] = float(
                  data[crypto]["USD"]["CHANGE24HOUR"] * rate)
                # multi_path_dict['{0}/Data/{1}/change_24hrs_percent'.format(crypto, currency)] = float(
                #         data[crypto]["USD"]["CHANGEPCT24HOUR"])
              else:
                multi_path_dict['{0}/Data/{1}/change_24hrs_fiat'.format(crypto, currency)] = float(
                  data[crypto][currency]["CHANGE24HOUR"])
                # multi_path_dict['{0}/Data/{1}/change_24hrs_percent'.format(crypto, currency)] = float(data[crypto][currency]["CHANGEPCT24HOUR"])

              multi_path_dict['{0}/Data/{1}/vol_24hrs_coin'.format(crypto, currency)] = float(
                data[crypto][currency]["VOLUME24HOUR"])
              # multi_path_dict['{0}/Data/{1}/vol_24hrs_fiat'.format(crypto, currency)] = float(data[crypto][currency]["VOLUME24HOURTO"])
              multi_path_dict['{0}/Data/{1}/high_24hrs'.format(crypto, currency)] = float(
                data[crypto][currency]["HIGH24HOUR"])
              multi_path_dict['{0}/Data/{1}/low_24hrs'.format(crypto, currency)] = float(
                data[crypto][currency]["LOW24HOUR"])
              multi_path_dict['{0}/Data/{1}/last_trade_volume'.format(crypto, currency)] = float(
                data[crypto][currency]["LASTVOLUME"])
              multi_path_dict['{0}/Data/{1}/last_trade_market'.format(crypto, currency)] = data[crypto][currency][
                "LASTMARKET"]
              # multi_path_dict['{0}/Data/{1}/supply'.format(crypto, currency)] = float(data[crypto][currency]["SUPPLY"])
              # multi_path_dict['{0}/Data/{1}/marketcap'.format(crypto, currency)] = float(data[crypto][currency]["MKTCAP"])

    for item in dict_chunks(multi_path_dict, 500):
      db.update(item)


def get_list_of_coins_with_rank():
  all_data = db.child("coins").get().val()
  return all_data
  # for data in all_data.each():
  #     return data.val()


def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in range(0, len(l), n):
    yield l[i:i + n]


def dict_chunks(data, SIZE=10000):
  it = iter(data)
  for i in range(0, len(data), SIZE):
    yield {k: data[k] for k in islice(it, SIZE)}


get_current_crypto_price()
