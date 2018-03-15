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
btc_markets = {"INR": {
                    "Zebpay": "zebpay_new/BTC",
                    "LocalBitcoins": "localbitcoins_BTC_INR",
                    "Coinsecure": "coinsecure",
                    "PocketBits": "pocketbits",
                    "Koinex": "koinex_BTC_INR",
                    "Throughbit": "throughbit_BTC_INR",
                    "Bitbns": "bitbns/BTC/INR",
                    "Coinome": "coinome_BTC_INR",
                    "Coindelta": "coindelta/BTC/INR"
                }, "USD": {
                    "Coinbase": "coinbase/BTC/USD",
                    "Kraken": "kraken_BTC_USD",
                    "Gemini": "gemini_BTC_USD",
                    "LocalBitcoins": "localbitcoins_BTC_USD",
                    "Bitfinex": "bitfinex_BTC_USD",
                    "Bitstamp": "bitstamp_BTC_USD",
                    "Kucoin": "kucoin/BTC/USDT"
                }, "GBP": {
                    "Coinbase": "coinbase/BTC/GBP",
                    "Kraken": "kraken_BTC_GBP",
                    "LocalBitcoins": "localbitcoins_BTC_GBP"
                }, "EUR": {
                   "Coinbase": "coinbase/BTC/EUR",
                   "LocalBitcoins": "localbitcoins_BTC_EUR",
                   "Kraken": "kraken_BTC_EUR"
                }, "JPY": {
                    "Kraken": "kraken_BTC_JPY"
                }, "CNY": {
                    "LocalBitcoins": "localbitcoins_BTC_CNY"
                }, "SGD": {
                    "LocalBitcoins": "localbitcoins_BTC_SGD",
                    "Coinbase": "coinbase/BTC/SGD"
                }, "ZAR": {
                    "LocalBitcoins": "localbitcoins_BTC_ZAR"
                }, "CAD": {
                    "Coinbase": "coinbase/BTC/CAD"
                }, "AUD": {
                    "Coinbase": "coinbase/BTC/AUD"
                }, "TRY": {}, "AED": {}, "BTC": {}, "ETH": {}}

eth_markets = {"INR": {
                    "Koinex": "koinex_ETH_INR",
                    "Throughbit": "throughbit_ETH_INR",
                    "Bitbns": "bitbns/ETH/INR",
                    "Coindelta": "coindelta/ETH/INR",
                    "Zebpay": "zebpay_new/ETH"
                }, "USD": {
                    "Coinbase": "coinbase/ETH/USD",
                    "Kraken": "kraken_ETH_USD",
                    "Gemini": "gemini_ETH_USD",
                    "Bitfinex": "bitfinex_ETH_USD",
                    "Bitstamp": "bitstamp_ETH_USD",
                    "Kucoin": "kucoin/ETH/USDT"
                },  "GBP": {
                    "Kraken": "kraken_ETH_GBP",
                    "Coinbase": "coinbase/ETH/GBP"
                }, "EUR": {
                    "Coinbase": "coinbase/ETH/EUR",
                    "Bitstamp": "bitstamp_ETH_EUR",
                    "Kraken": "kraken_ETH_EUR"
                },  "JPY": {
                    "Kraken": "kraken_ETH_JPY"
                }, "CNY": {}, "SGD": {
                    "Coinbase": "coinbase/ETH/SGD"
                }, "ZAR": {}, "CAD": {
                    "Coinbase": "coinbase/ETH/CAD"
                }, "AUD": {
                    "Coinbase": "coinbase/ETH/AUD"
                }, "TRY": {}, "AED": {},
                "BTC": {
                    "Kucoin": "kucoin/ETH/BTC",
                    "Coindelta": "coindelta/ETH/BTC"
                },
                "ETH": {}}

ltc_markets = {"INR": {
                    "Zebpay": "zebpay_new/LTC",
                    "Koinex": "koinex_LTC_INR",
                    "Coinome": "coinome_LTC_INR",
                    "Coindelta": "coindelta/LTC/INR",
                    "Bitbns": "bitbns/LTC/INR"
                }, "USD": {
                    "Coinbase": "coinbase/LTC/USD",
                    "Kraken": "kraken_LTC_USD",
                    "Bitfinex": "bitfinex_LTC_USD",
                    "Bitstamp": "bitstamp_LTC_USD",
                    "Kucoin": "kucoin/LTC/USDT"
                }, "GBP": {
                    "Coinbase": "coinbase/LTC/GBP"
                },
                "EUR": {
                    "Coinbase": "coinbase/LTC/EUR",
                    "Bitstamp": "bitstamp_LTC_EUR",
                    "Kraken": "kraken_LTC_EUR"
                },
                "JPY": {},
                "CNY": {},
                "SGD": {
                    "Coinbase": "coinbase/LTC/SGD"
                }, "ZAR": {},
                "CAD": {
                    "Coinbase": "coinbase/LTC/CAD"
                }, "TRY": {},
                "AUD": {
                    "Coinbase": "coinbase/LTC/AUD"
                }, "AED": {},
                "BTC": {
                    "Kucoin": "kucoin/LTC/BTC",
                    "Coindelta": "coindelta/LTC/BTC"
                },
                "ETH": {
                    "Kucoin": "kucoin/LTC/ETH"
                }}

xrp_markets = {"INR": {
                    "Zebpay": "zebpay_new/XRP",
                    "Koinex": "koinex_XRP_INR",
                    "Bitbns": "bitbns/XRP/INR",
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
                },
                "ETH": {}, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}}

bch_markets = {"INR": {
                    "Zebpay": "zebpay_new/BCH",
                    "Koinex": "koinex_BCH_INR",
                    "Coinome": "coinome_BCH_INR",
                    "Coindelta": "coindelta/BCH/INR",
                    "Bitbns": "bitbns/BCH/INR",
                }, "USD": {
                    "Bitfinex": "bitfinex_BCH_USD",
                    "Coinbase": "coinbase/BCH/USD"
                }, "GBP": {
                    "Coinbase": "coinbase/BCH/GBP"
                }, "EUR": {
                    "Coinbase": "coinbase/BCH/EUR"
                }, "JPY": {

                }, "CNY": {

                }, "SGD": {
                    "Coinbase": "coinbase/BCH/SGD"
                }, "ZAR": {

                }, "CAD": {
                    "Coinbase": "coinbase/BCH/CAD"
                }, "AUD": {
                    "Coinbase": "coinbase/BCH/AUD"
                }, "TRY": {}, "AED": {},
                "BTC": {
                    "Kucoin": "kucoin/BCH/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/BCH/ETH"
                }}

omg_markets = { "INR": {
                    "Koinex": "koinex_OMG_INR",
                    "Coindelta": "coindelta/OMG/INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/OMG/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/OMG/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

req_markets = { "INR": {
                    "Koinex": "koinex_REQ_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/REQ/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/REQ/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

zrx_markets = { "INR": {
                    "Koinex": "koinex_ZRX_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

gnt_markets = { "INR": {
                    "Koinex": "koinex_GNT_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

bat_markets = { "INR": {
                    "Koinex": "koinex_BAT_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

ae_markets = { "INR": {
                    "Koinex": "koinex_AE_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

rpx_markets = { "INR": {
                    "Bitbns": "bitbns/RPX/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/RPX/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/RPX/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
dbc_markets = { "INR": {
                    "Bitbns": "bitbns/DBC/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/DBC/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/DBC/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
xmr_markets = { "INR": {
                    "Bitbns": "bitbns/XMR/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
doge_markets = { "INR": {
                    "Bitbns": "bitbns/DOGE/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
sia_markets = { "INR": {
                    "Bitbns": "bitbns/SIA/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

xlm_markets = { "INR": {
                    "Bitbns": "bitbns/XLM/INR",
                    "Koinex": "koinex_XLM_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

neo_markets = { "INR": {
                    "Bitbns": "bitbns/NEO/INR",
                    "Koinex": "koinex_NEO_INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/NEO/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/NEO/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

trx_markets = { "INR": {
                    "Koinex": "koinex_TRX_INR",
                    "Bitbns": "bitbns/TRX/INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

dgb_markets = { "INR": {
                    "Coinome": "coinome_DGB_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/DGB/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/DGB/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

zec_markets = { "INR": {
                    "Coinome": "coinome_ZEC_INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

qtum_markets = { "INR": {
                    "Coindelta": "coindelta/QTUM/INR",
                    "Coinome": "coinome_QTUM_INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/QTUM/BTC"
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

dash_markets = { "INR": {
                    "Coinome": "coinome_DASH_INR",
                    "Bitbns": "bitbns/DASH/INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/DASH/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/DASH/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

gas_markets = { "INR": {
                    "Bitbns": "bitbns/GAS/INR",
                    "Koinex": "koinex_GAS_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/GAS/BTC"
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

btg_markets = { "INR": {
                    "Coinome": "coinome_DGB_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/BTG/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/BTG/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

crypto_with_markets_list = ["BTC", "BCH", "ETH", "XRP", "LTC", "OMG", "REQ", "ZRX", "GNT", "BAT",
                            "AE", "RPX", "DBC", "XMR", "DOGE", "SIA", "XLM", "NEO", "TRX", "DGB",
                            "ZEC", "QTUM", "GAS", "DASH", "BTG"]

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
                            elif crypto == "OMG":
                                dict[crypto][currency]["markets"] = omg_markets[currency]
                            elif crypto == "REQ":
                                dict[crypto][currency]["markets"] = req_markets[currency]
                            elif crypto == "ZRX":
                                dict[crypto][currency]["markets"] = zrx_markets[currency]
                            elif crypto == "BAT":
                                dict[crypto][currency]["markets"] = bat_markets[currency]
                            elif crypto == "GNT":
                                dict[crypto][currency]["markets"] = gnt_markets[currency]
                            elif crypto == "AE":
                                dict[crypto][currency]["markets"] = ae_markets[currency]
                            elif crypto == "RPX":
                                dict[crypto][currency]["markets"] = rpx_markets[currency]
                            elif crypto == "DBC":
                                dict[crypto][currency]["markets"] = dbc_markets[currency]
                            elif crypto == "XMR":
                                dict[crypto][currency]["markets"] = xmr_markets[currency]
                            elif crypto == "DOGE":
                                dict[crypto][currency]["markets"] = doge_markets[currency]
                            elif crypto == "SIA":
                                dict[crypto][currency]["markets"] = sia_markets[currency]
                            elif crypto == "XLM":
                                dict[crypto][currency]["markets"] = xlm_markets[currency]
                            elif crypto == "NEO":
                                dict[crypto][currency]["markets"] = neo_markets[currency]
                            elif crypto == "TRX":
                                dict[crypto][currency]["markets"] = trx_markets[currency]
                            elif crypto == "DGB":
                                dict[crypto][currency]["markets"] = dgb_markets[currency]
                            elif crypto == "ZEC":
                                dict[crypto][currency]["markets"] = zec_markets[currency]
                            elif crypto == "QTUM":
                                dict[crypto][currency]["markets"] = qtum_markets[currency]
                            elif crypto == "DASH":
                                dict[crypto][currency]["markets"] = dash_markets[currency]
                            elif crypto == "GAS":
                                dict[crypto][currency]["markets"] = gas_markets[currency]
                            elif crypto == "BTG":
                                dict[crypto][currency]["markets"] = btg_markets[currency]
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


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

get_current_crypto_price()


