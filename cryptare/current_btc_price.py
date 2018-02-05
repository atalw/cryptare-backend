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
btc_markets = {"INR": {"Zebpay": "zebpay", "LocalBitcoins": "localbitcoins_BTC_INR", "Coinsecure": "coinsecure",
                "PocketBits": "pocketbits", "Koinex": "koinex_BTC_INR", "Throughbit": "throughbit_BTC_INR"},
                "USD": {"Coinbase": "coinbase_BTC_USD", "Kraken": "kraken_BTC_USD", "Gemini": "gemini_BTC_USD",
                "LocalBitcoins": "localbitcoins_BTC_USD", "Bitfinex": "bitfinex_BTC_USD", "Bitstamp": "bitstamp_BTC_USD"},
               "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {}}

eth_markets = {"INR": {"Koinex": "koinex_ETH_INR"},
                "USD": {}, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {}}

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
                    if crypto in data:
                        if currency != "INR" and (crypto != "BTC" and crypto != "ETH" and crypto != "LTC" and crypto != "XRP" and crypto != "BCH"):
                            dict[crypto][currency]["price"] = float(data[crypto][currency]["PRICE"])
                        else:
                            dict[crypto][currency]["price"] = float(db.child(crypto).child("Data").child(currency).child("price").get().val())
                        dict[crypto][currency]["timestamp"] = float(data[crypto][currency]["LASTUPDATE"])
                        dict[crypto][currency]["change_24hrs_fiat"] = float(data[crypto][currency]["CHANGE24HOUR"])
                        dict[crypto][currency]["change_24hrs_percent"] = float(data[crypto][currency]["CHANGEPCT24HOUR"])
                        dict[crypto][currency]["vol_24hrs_coin"] = float(data[crypto][currency]["VOLUME24HOUR"])
                        dict[crypto][currency]["vol_24hrs_fiat"] = float(data[crypto][currency]["VOLUME24HOURTO"])
                        dict[crypto][currency]["high_24hrs"] = float(data[crypto][currency]["HIGH24HOUR"])
                        dict[crypto][currency]["low_24hrs"] = float(data[crypto][currency]["LOW24HOUR"])
                        dict[crypto][currency]["last_trade_volume"] = float(data[crypto][currency]["LASTVOLUME"])
                        dict[crypto][currency]["last_trade_market"] = data[crypto][currency]["LASTMARKET"]
                        dict[crypto][currency]["supply"] = float(data[crypto][currency]["SUPPLY"])
                        dict[crypto][currency]["marketcap"] = float(data[crypto][currency]["MKTCAP"])
                        if crypto == "BTC":
                            dict[crypto][currency]["markets"] = btc_markets[currency]
                        elif crypto == "ETH":
                            dict[crypto][currency]["markets"] = eth_markets[currency]
                        else:
                            dict[crypto][currency]["markets"] = {}

            for coin in dict.keys():
                data = {"Data": dict[coin]}
                title = coin
                db.child(title).update(data)

def get_list_of_coins_with_rank():
    all_data = db.child("coins").order_by_key().limit_to_last(1).get()
    for data in all_data.each():
        return data.val()


get_current_crypto_price()