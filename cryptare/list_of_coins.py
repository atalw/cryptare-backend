import requests
import pyrebase
from itertools import islice
import time

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

supported_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                        "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                        "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD",
                        "ZAR"]

multi_path_dict = {}

illegal_characters = ["-", "."]

def update_list_of_coins_with_rank():

    for currency in supported_currencies:
        url = "https://api.coinmarketcap.com/v1/ticker/?convert={}&limit=50".format(currency)

        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            for coin in json:
                symbol = coin["symbol"]
                if symbol == "MIOTA":
                    symbol = "IOT"
                elif symbol == "NANO":
                    symbol = "XRB"

                if not any(substring in symbol for substring in illegal_characters) and not any(substring in coin["name"] for substring in illegal_characters):
                    multi_path_dict['coins/{}/rank'.format(symbol)] = float(coin["rank"])
                    multi_path_dict['coins/{}/name'.format(symbol)] = coin["name"]
                else:
                    continue

                try:
                    icon_url = storage.child("icons/{}.png".format(symbol.lower())).get_url(token=None)
                    multi_path_dict['coins/{}/icon_url'.format(symbol)] = icon_url
                except:
                    pass

                lower_currency = currency.lower()
                multi_path_dict['{0}/Data/{1}/price'.format(symbol, currency)] = float(coin['price_{}'.format(lower_currency)])
                multi_path_dict['{0}/Data/{1}/vol_24hrs_fiat'.format(symbol, currency)] = float(coin['24h_volume_{}'.format(lower_currency)])
                multi_path_dict['{0}/Data/{1}/supply'.format(symbol, currency)] = float(coin['available_supply'])
                multi_path_dict['{0}/Data/{1}/marketcap'.format(symbol, currency)] = float(coin['market_cap_{}'.format(lower_currency)])
                multi_path_dict['{0}/Data/{1}/change_24hrs_percent'.format(symbol, currency)] = float(coin['percent_change_24h'])
                multi_path_dict['{0}/Data/{1}/timestamp'.format(symbol, currency)] = time.time()

        else:
            return "list coin error"

    for item in dict_chunks(multi_path_dict, 500):
        db.update(item)

def dict_chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

update_list_of_coins_with_rank()


