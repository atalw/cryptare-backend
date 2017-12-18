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

coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR"]


def update_current_bitcoin_price():
    for currency in currencies:
        dict = get_current_bitcoin_price(currency)
        if dict is not None:
            # store price and timestamp
            for coin in dict.keys():
                currency = dict[coin]["currency"]
                data = {"timestamp": dict[coin]["timestamp"],
                        "price": dict[coin]["price_{}".format(currency)],
                        "price_btc": dict[coin]["price_btc"],
                        "available_supply": dict[coin]["available_supply"],
                        "total_supply": dict[coin]["total_supply"],
                        "max_supply": dict[coin]["max_supply"],
                        "percentage_change_1h": dict[coin]["percentage_change_1h"],
                        "percentage_change_24h": dict[coin]["percentage_change_24h"],
                        "percentage_change_7d": dict[coin]["percentage_change_7d"],
                        "vol_24hrs_{}".format(currency): dict[coin]["vol_24hrs_{}".format(currency)],
                        "market_cap_{}".format(currency): dict[coin]["market_cap_{}".format(currency)]
                        }
                title = "current_{0}_price_{1}".format(coin, currency)
                db.child(title).push(data)
        else:
            print("current price error")



def get_current_bitcoin_price(currency):
    url = "https://api.coinmarketcap.com/v1/ticker/?convert={}&limit=10".format(currency)
    r = requests.get(url)
    dict = {}
    if r.status_code == 200:
        json = r.json()
        for index in range(len(json)):
            symbol = json[index]["symbol"]
            dict[symbol] = {}
            dict[symbol]["currency"] = currency
            dict[symbol]["price_{}".format(currency)] = float(json[index]["price_{}".format(currency.lower())])
            dict[symbol]["price_btc"] = float(json[index]["price_btc"])
            dict[symbol]["available_supply"] = json[index]["available_supply"]
            dict[symbol]["total_supply"] = json[index]["total_supply"]
            dict[symbol]["max_supply"] = json[index]["max_supply"]
            dict[symbol]["percentage_change_1h"] = float(json[index]["percent_change_1h"])
            dict[symbol]["percentage_change_24h"] = float(json[index]["percent_change_24h"])
            dict[symbol]["percentage_change_7d"] = float(json[index]["percent_change_7d"])
            dict[symbol]["vol_24hrs_{}".format(currency)] = float(json[index]["24h_volume_{}".format(currency.lower())])
            dict[symbol]["market_cap_{}".format(currency)] = json[index]["market_cap_{}".format(currency.lower())]
            dict[symbol]["timestamp"] = float(json[index]["last_updated"])

        return dict
    return None


update_current_bitcoin_price()
