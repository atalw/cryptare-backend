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
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR", "BTC"]
btc_markets = {"INR": {
                    "Zebpay": "zebpay_new/BTC",
                    "LocalBitcoins": "localbitcoins_BTC_INR",
                    "Coinsecure": "coinsecure",
                    "PocketBits": "pocketbits",
                    "Koinex": "koinex_BTC_INR",
                    "Throughbit": "throughbit_BTC_INR",
                    "Bitbns": "bitbns_BTC_INR",
                    "Coinome": "coinome_BTC_INR",
                    "Coindelta": "coindelta/BTC/INR"
                }, "USD": {
                    "Coinbase": "coinbase_BTC_USD",
                    "Kraken": "kraken_BTC_USD",
                    "Gemini": "gemini_BTC_USD",
                    "LocalBitcoins": "localbitcoins_BTC_USD",
                    "Bitfinex": "bitfinex_BTC_USD",
                    "Bitstamp": "bitstamp_BTC_USD",
                    "Kucoin": "kucoin/BTC/USDT"
                }, "GBP": {
                    "Coinbase": "coinbase_BTC_GBP",
                    "Kraken": "kraken_BTC_GBP",
                    "LocalBitcoins": "localbitcoins_BTC_GBP"
                }, "EUR": {
                   "Coinbase": "coinbase_BTC_EUR",
                   "LocalBitcoins": "localbitcoins_BTC_EUR",
                   "Kraken": "kraken_BTC_EUR"
                }, "JPY": {
                    "Kraken": "kraken_BTC_JPY"
                }, "CNY": {
                    "LocalBitcoins": "localbitcoins_BTC_CNY"
                }, "SGD": {
                    "LocalBitcoins": "localbitcoins_BTC_SGD"
                }, "ZAR": {
                    "LocalBitcoins": "localbitcoins_BTC_ZAR"
                }, "BTC": {}}

eth_markets = {"INR": {
                    "Koinex": "koinex_ETH_INR",
                    "Throughbit": "throughbit_ETH_INR",
                    "Bitbns": "bitbns_ETH_INR",
                    "Coindelta": "coindelta/ETH/INR"
                }, "USD": {
                    "Coinbase": "coinbase_ETH_USD",
                    "Kraken": "kraken_ETH_USD",
                    "Gemini": "gemini_ETH_USD",
                    "Bitfinex": "bitfinex_ETH_USD",
                    "Bitstamp": "bitstamp_ETH_USD",
                    "Kucoin": "kucoin/ETH/USDT"
                },  "GBP": {
                    "Kraken": "kraken_ETH_GBP"
                }, "EUR": {
                    "Coinbase": "coinbase_ETH_EUR",
                    "Bitstamp": "bitstamp_ETH_EUR",
                    "Kraken": "kraken_ETH_EUR"
                },  "JPY": {
                    "Kraken": "kraken_ETH_JPY"
                }, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/ETH/BTC",
                    "Coindelta": "coindelta/ETH/BTC"
                }
                }

ltc_markets = {"INR": {
                    "Zebpay": "zebpay_new/LTC",
                    "Koinex": "koinex_LTC_INR",
                    "Coinome": "coinome_LTC_INR",
                    "Coindelta": "coindelta/BTC/INR"
                }, "USD": {
                    "Coinbase": "coinbase_LTC_USD",
                    "Kraken": "kraken_LTC_USD",
                    "Bitfinex": "bitfinex_LTC_USD",
                    "Bitstamp": "bitstamp_LTC_USD",
                    "Kucoin": "kucoin/LTC/USDT"
                }, "GBP": {},
                "EUR": {
                    "Coinbase": "coinbase_LTC_EUR",
                    "Bitstamp": "bitstamp_LTC_EUR",
                    "Kraken": "kraken_LTC_EUR"
                },
                "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/LTC/BTC",
                    "Coindelta": "coindelta/LTC/BTC"
                }}

xrp_markets = {"INR": {
                    "Zebpay": "zebpay_new/XRP",
                    "Koinex": "koinex_XRP_INR",
                    "Bitbns": "bitbns_XRP_INR",
                    "Coindelta": "coindelta/XRP/INR"
                },  "USD": {
                    "Bitfinex": "bitfinex_XRP_USD",
                    "Bitstamp": "bitstamp_XRP_USD"
                }, "GBP": {

                }, "EUR": {
                    "Bitstamp": "bitstamp_XRP_EUR",
                },  "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Coindelta": "coindelta/XRP/BTC"
                }}

bch_markets = {"INR": {
                    "Zebpay": "zebpay_new/BCH",
                    "Koinex": "koinex_BCH_INR",
                    "Coinome": "coinome_BCH_INR",
                    "Coindelta": "coindelta/BCH/INR"
                }, "USD": {
                    "Bitfinex": "bitfinex_BCH_USD",
                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {}, "BTC": {}}

indian_crypto_list = ["BTC", "BCH", "ETH", "XRP", "LTC"]

def get_current_crypto_price():
    dict = get_list_of_coins_with_rank()
    if dict is not None:
        crypto_list = list()
        for i in dict.keys():
            crypto_list.append(i)
        crypto_list_string = ",".join(crypto_list)
        currency_list_string = ",".join(currencies)

        exchange_rate_url = "https://api.fixer.io/latest?symbols=INR&base=USD"
        r = requests.get(exchange_rate_url)
        if r.status_code == 200:
            exchange_json = r.json()
            rate = exchange_json["rates"]["INR"]

        url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(crypto_list_string, currency_list_string)
        r = requests.get(url)
        if r.status_code == 200:
            json = r.json()
            data = json["RAW"]
            for crypto in crypto_list:
                for currency in currencies:
                    dict[crypto][currency] = {}
                    if crypto in data:
                        if currency == "INR" and crypto in indian_crypto_list:
                            dict[crypto][currency]["price"] = float(
                                db.child(crypto).child("Data").child(currency).child("price").get().val())
                            dict[crypto][currency]["timestamp"] = float(
                                db.child(crypto).child("Data").child(currency).child("timestamp").get().val())
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
                        if crypto == "BTC":
                            dict[crypto][currency]["markets"] = btc_markets[currency]
                        elif crypto == "ETH":
                            dict[crypto][currency]["markets"] = eth_markets[currency]
                        elif crypto == "LTC":
                            dict[crypto][currency]["markets"] = ltc_markets[currency]
                        elif crypto == "XRP":
                            dict[crypto][currency]["markets"] = xrp_markets[currency]
                        elif crypto == "BCH":
                            dict[crypto][currency]["markets"] = bch_markets[currency]
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