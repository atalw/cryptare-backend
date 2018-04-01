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
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR", "BTC", "ETH", "CAD", "AUD", "TRY", "AED"]

crypto_with_markets_list = ["BTC", "BCH", "ETH", "XRP", "LTC", "OMG", "REQ", "ZRX", "GNT", "BAT",
                            "AE", "RPX", "DBC", "XMR", "DOGE", "SIA", "XLM", "NEO", "TRX", "DGB",
                            "ZEC", "QTUM", "GAS", "DASH", "BTG", "IOT", "ZIL", "ETN", "ONT", "KNC",
                            "EOS", "POLY", "AION", "NCASH", "ICX", "VEN"]

def get_current_crypto_price():
    dict = get_list_of_coins_with_rank()
    if dict is not None:
        crypto_list = list()
        for i in dict.keys():
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
            url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(crypto_list_string[index], currency_list_string)
            r = requests.get(url)
            if r.status_code == 200:
                json = r.json()
                data = json["RAW"]
                for crypto in crypto_list:
                    for currency in currencies:
                        dict[crypto][currency] = {}
                        if crypto in data and currency in data[crypto]:
                            if currency == "INR" and crypto in crypto_with_markets_list:
                                old_price = db.child(crypto).child("Data").child(currency).child("price").get().val()
                                old_timestamp = db.child(crypto).child("Data").child(currency).child("timestamp").get().val()
                                if old_price is not None:
                                    dict[crypto][currency]["price"] = float(old_price)
                                else:
                                    dict[crypto][currency]["price"] = float(data[crypto][currency]["PRICE"])

                                if old_timestamp is not None:
                                    dict[crypto][currency]["timestamp"] =  float(old_timestamp)
                                else:
                                    dict[crypto][currency]["timestamp"] = float(data[crypto][currency]["LASTUPDATE"])

                            else:

                                dict[crypto][currency]["price"] = float(data[crypto][currency]["PRICE"])
                                dict[crypto][currency]["timestamp"] = float(data[crypto][currency]["LASTUPDATE"])

                            if currency == "INR" and rate is not None:
                                    dict[crypto]["INR"]["change_24hrs_fiat"] = float(
                                        data[crypto]["USD"]["CHANGE24HOUR"]*rate)
                                    dict[crypto][currency]["change_24hrs_percent"] = float(
                                        data[crypto]["USD"]["CHANGEPCT24HOUR"])
                            else:
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
                            try:
                                markets = db.child(crypto).child("Data").child(currency).child("markets").get().val()
                            except:
                                markets = {}
                            dict[crypto][currency]["markets"] = markets

        for coin in dict.keys():
            data = {"Data": dict[coin]}
            title = coin
            db.child(title).update(data)

def get_list_of_coins_with_rank():
    all_data = db.child("coins").order_by_key().limit_to_last(1).get()
    for data in all_data.each():
        return data.val()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

get_current_crypto_price()


