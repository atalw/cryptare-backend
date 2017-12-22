import requests
import pyrebase
import json
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


def get_current_crypto_price():
    dict = get_list_of_coins_with_rank()
    if dict is not None:
        crypto_list = list()
        for i in dict.keys():
            crypto_list.append(i)
        crypto_list_string = ",".join(crypto_list)
        currency_list_string = ",".join(currencies)
        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(crypto_list_string, currency_list_string)
        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            data = json["RAW"]
            for crypto in crypto_list:
                for currency in currencies:
                    dict[crypto][currency] = {}
                    if crypto != "MIOTA" and crypto != "VET":
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
                data = {"Data": dict[coin]}
                title = coin
                db.child(title).update(data)

def get_list_of_coins_with_rank():
    all_data = db.child("coins").order_by_key().limit_to_last(1).get()
    for data in all_data.each():
        return data.val()


get_current_crypto_price()