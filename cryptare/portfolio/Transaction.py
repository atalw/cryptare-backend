import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import requests

from diskcache import Cache
from diskcache import Index

# from cryptare.portfolio.portfolio_data import db

class Crypto_Transaction:

    if not len(firebase_admin._apps):
        cred = credentials.Certificate('../../service_account_info/Cryptare-9d04b184ba96.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://atalwcryptare.firebaseio.com/'
        })
    else:
        firebase_admin.get_app()

    ref = db.reference()

    cache = Cache('/tmp/exchange_prices')
    cache_store_time = 60 * 10

    supported_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                            "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                            "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD",
                            "USD", "ZAR", "BTC", "ETH"]

    def __init__(self, type, coin, trading_pair, exchange, cost_per_coin, total_coins, fees, total_cost):
        self.type = type
        self.coin = coin
        self.trading_pair = trading_pair
        self.exchange = exchange
        self.cost_per_coin = cost_per_coin
        self.total_coins = total_coins
        self.fees = fees
        self.total_cost = total_cost

    def return_invested_cost(self):
        if self.type == "buy":
            return self.total_cost
        elif self.type == "sell":
            return -self.total_cost

    def return_current_cost(self):
        # get current price of coin from exchange (check cache first)
        # calculate total cost
        print(self.exchange, self.coin, self.trading_pair)
        self.cache.expire()

        if self.exchange == "None":
            key = '{}/228/{}/price'.format(self.coin, self.trading_pair)
        else:
            key = '{}/{}/{}/last_price'.format(self.exchange, self.coin, self.trading_pair)

        index = Index.fromcache(self.cache)
        print(dict(index))
        if key in index:
            print(key, index)
            current_coin_price = dict(index[key])
        else:
            current_coin_price = self.ref.get(key)
            if current_coin_price is not None:
                self.cache.set(key, current_coin_price, expire=self.cache_store_time)
            else:
                print("its none obv")

        total_cost = (self.total_coins * current_coin_price) - self.fees

        if self.trading_pair == "USD" or self.trading_pair == "USDT":
            # return total cost
            return total_cost
        else:
            # if trading pair is crypto
            ## get crypto/USD price
            # else
            ## get currency/USD price

            if self.trading_pair in self.supported_currencies:
                rate = self.get_fiat_usd_rate(self.trading_pair)
                total_cost_usd = total_cost * rate
                return total_cost_usd
            else:
                key = '{}/{}/USD/last_price'.format(self.exchange, self.trading_pair)

                if key in index:
                    trading_pair_usd_price = dict(index[key])
                else:
                    key = '{}/{}/USDT/last_price'.format(self.exchange, self.trading_pair)

                    if key in index:
                        trading_pair_usd_price = dict(index[key])
                    else:
                        trading_pair_usd_price = self.ref.get(key)

                total_cost_usd = total_cost * trading_pair_usd_price
                return total_cost_usd


    def get_fiat_usd_rate(self, currency):
        exchange_rate_url = "https://api.fixer.io/latest?symbols={}&base=USD".format(currency)
        r = requests.get(exchange_rate_url)
        if r.status_code == 200:
            exchange_json = r.json()
            return exchange_json["rates"]["INR"]
        else:
            print("error")
            return

class Fiat_Transaction:

    def __init__(self, type, currency, amount, fees, total_cost):
        self.type = type
        self.currency = currency
        self.amount = amount
        self.fees = fees
        self.total_cost = total_cost

    def return_invested_cost(self):
        # print(self.type, self.total_cost)
        if self.type == "deposit":
            return self.total_cost
        elif self.type == "withdraw":
            return -self.total_cost