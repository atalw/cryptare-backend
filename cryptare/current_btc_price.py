import requests
import pyrebase
import time

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
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR"]

#
# def update_current_bitcoin_price():
#     for currency in currencies:
#         dict = get_current_bitcoin_price(currency)
#         if dict is not None:
#             for coin in dict.keys():
#                 currency = dict[coin]["currency"]
#                 data = {"timestamp": dict[coin]["timestamp"],
#                         "price": dict[coin]["price_{}".format(currency)],
#                         "price_btc": dict[coin]["price_btc"],
#                         "available_supply": dict[coin]["available_supply"],
#                         "total_supply": dict[coin]["total_supply"],
#                         "max_supply": dict[coin]["max_supply"],
#                         "percentage_change_1h": dict[coin]["percentage_change_1h"],
#                         "percentage_change_24h": dict[coin]["percentage_change_24h"],
#                         "percentage_change_7d": dict[coin]["percentage_change_7d"],
#                         "vol_24hrs_{}".format(currency): dict[coin]["vol_24hrs_{}".format(currency)],
#                         "market_cap_{}".format(currency): dict[coin]["market_cap_{}".format(currency)]
#                         }
#                 title = "current_{0}_price_{1}".format(coin, currency)
#                 db.child(title).push(data)
#         else:
#             print("current price error")
#
#
#
# def get_current_bitcoin_price(currency):
#     url = "https://api.coinmarketcap.com/v1/ticker/?convert={}&limit=10".format(currency)
#     r = requests.get(url)
#     dict = {}
#     if r.status_code == 200:
#         json = r.json()
#         for index in range(len(json)):
#             symbol = json[index]["symbol"]
#             dict[symbol] = {}
#             dict[symbol]["currency"] = currency
#             dict[symbol]["price_{}".format(currency)] = float(json[index]["price_{}".format(currency.lower())])
#             dict[symbol]["price_btc"] = float(json[index]["price_btc"])
#             dict[symbol]["available_supply"] = json[index]["available_supply"]
#             dict[symbol]["total_supply"] = json[index]["total_supply"]
#             dict[symbol]["max_supply"] = json[index]["max_supply"]
#             dict[symbol]["percentage_change_1h"] = float(json[index]["percent_change_1h"])
#             dict[symbol]["percentage_change_24h"] = float(json[index]["percent_change_24h"])
#             dict[symbol]["percentage_change_7d"] = float(json[index]["percent_change_7d"])
#             dict[symbol]["vol_24hrs_{}".format(currency)] = float(json[index]["24h_volume_{}".format(currency.lower())])
#             dict[symbol]["market_cap_{}".format(currency)] = json[index]["market_cap_{}".format(currency.lower())]
#             dict[symbol]["timestamp"] = float(json[index]["last_updated"])
#
#         return dict
#     return None


def get_current_crypto_price():
    dict = get_list_of_coins_with_rank()
    if dict is not None:
        print(dict)
        crypto_list = list()
        for i in dict.keys():
            crypto_list.append(i)
        crypto_list_string = ",".join(crypto_list)
        currency_list_string = ",".join(currencies)
        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(crypto_list_string, currency_list_string)
        print(url)
        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            data = json["RAW"]
            for crypto in crypto_list:
                for currency in currencies:
                    dict[crypto][currency] = {}
                    if crypto != "MIOTA":
                        dict[crypto][currency]["price"] = data[crypto][currency]["PRICE"]
                        dict[crypto][currency]["timestamp"] = data[crypto][currency]["LASTUPDATE"]
                        dict[crypto][currency]["change_24hrs_fiat"] = data[crypto][currency]["CHANGE24HOUR"]
                        dict[crypto][currency]["change_24hrs_percent"] = data[crypto][currency]["CHANGEPCT24HOUR"]
                        dict[crypto][currency]["vol_24hrs_currency"] = data[crypto][currency]["VOLUME24HOUR"]
                        dict[crypto][currency]["vol_24hrs_total"] = data[crypto][currency]["VOLUME24HOURTO"]
                        dict[crypto][currency]["high_24hrs"] = data[crypto][currency]["HIGH24HOUR"]
                        dict[crypto][currency]["low_24hrs"] = data[crypto][currency]["LOW24HOUR"]
                        dict[crypto][currency]["last_trade_volume"] = data[crypto][currency]["LASTVOLUME"]
                        dict[crypto][currency]["last_trade_market"] = data[crypto][currency]["LASTMARKET"]
                        dict[crypto][currency]["supply"] = data[crypto][currency]["SUPPLY"]
                        dict[crypto][currency]["marketcap"] = data[crypto][currency]["MKTCAP"]

            for coin in dict.keys():
                data = dict[coin]
                title = coin
                db.child(title).push(data)

def get_list_of_coins_with_rank():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=50"
    r = requests.get(url)
    dict = {}
    if r.status_code == 200:
        json = r.json()
        for index in range(len(json)):
            symbol = json[index]["symbol"]
            dict[symbol] = {}
            dict[symbol]["rank"] = float(json[index]["rank"])
        return dict


# update_current_bitcoin_price()
get_current_crypto_price()