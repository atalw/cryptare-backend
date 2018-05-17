import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import requests

from diskcache import Cache
from diskcache import Index


class CryptoTransaction:

    if not len(firebase_admin._apps):
        cred = credentials.Certificate('../../service_account_info/Cryptare-9d04b184ba96.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://atalwcryptare.firebaseio.com/'
        })
    else:
        firebase_admin.get_app()

    ref = db.reference()

    cache = Cache('/tmp/exchange_prices')
    cache_store_time = 60

    supported_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP",
                            "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK",
                            "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD",
                            "USD", "ZAR"]

    def __init__(self, transaction_type, coin, trading_pair, exchange_db_title, total_coins, fees, total_cost_usd):
        self.transaction_type = transaction_type
        self.coin = coin
        self.trading_pair = trading_pair
        self.exchange_db_title = exchange_db_title
        self.total_coins = total_coins
        self.fees = fees
        self.total_cost_usd = total_cost_usd

    def return_invested_cost(self):
        if self.transaction_type == "buy" or self.transaction_type == "cryptoBuy":
            return self.total_cost_usd
        elif self.transaction_type == "sell" or self.transaction_type == "cryptoSell":
            return -self.total_cost_usd

    def return_current_cost(self):
        # get current price of coin from exchange (check cache first)
        # calculate total cost
        # print(self.exchange_db_title, self.coin, self.trading_pair)
        self.cache.expire()

        if self.transaction_type == 'sell' or self.transaction_type == 'cryptoSell':
            return -self.total_cost_usd

        if self.exchange_db_title == "none" or self.transaction_type == 'cryptoBuy':
            key = '{}/Data/{}/price'.format(self.coin, self.trading_pair)
        else:
            key = '{}/buy_price'.format(self.exchange_db_title)

        index = Index.fromcache(self.cache)
        if key in index:
            # print(key, index, index[key])
            current_coin_price = index[key]
        else:
            current_coin_price = self.ref.child(key).get()
            if current_coin_price is not None:
                self.cache.set(key, current_coin_price, expire=self.cache_store_time)
            else:
                print("its none oh shit", key)

        total_cost = (self.total_coins * current_coin_price) - self.fees

        if self.trading_pair == "USD":
            return total_cost
        else:
            if self.trading_pair in self.supported_currencies:
                rate = get_fiat_usd_rate(self.trading_pair)
                total_cost_usd = total_cost * rate
                return total_cost_usd
            else:
                if self.exchange_db_title == "none":
                    key = '{}/Data/USD/price'.format(self.trading_pair)

                    if key in index:
                        trading_pair_usd_price = index[key]
                    else:
                        trading_pair_usd_price = self.ref.child(key).get()
                else:
                    db_title_parts = self.exchange_db_title.split("/")
                    key = '{}/{}/USD/buy_price'.format(db_title_parts[0], self.trading_pair)

                    if key in index:
                        trading_pair_usd_price = index[key]
                    else:
                        key = '{}/{}/USDT/buy_price'.format(db_title_parts[0], self.trading_pair)

                        if key in index:
                            trading_pair_usd_price = index[key]
                        else:
                            key = '{}/Data/USD/price'.format(self.trading_pair)
                            trading_pair_usd_price = self.ref.child(key).get()
                            if trading_pair_usd_price is None:
                                key = '{}/{}/USDT/buy_price'.format(db_title_parts[0], self.trading_pair)
                                trading_pair_usd_price = self.ref.child(key).get()
                                if trading_pair_usd_price is None:
                                    print('ERRORRRR SHOULD NEVER BE HERE', db_title_parts, key)
                                    return 0

                total_cost_usd = total_cost * trading_pair_usd_price

                return total_cost_usd

    @staticmethod
    def return_value_from_type(value, transaction_type):
        if transaction_type == "buy" or transaction_type == "cryptoBuy":
            return value
        elif transaction_type == "sell" or transaction_type == "cryptoSell":
            return -value


class FiatTransaction:

    def __init__(self, transaction_type, currency, amount, fees):
        self.transaction_type = transaction_type
        self.currency = currency
        self.amount = amount
        self.fees = fees
        self.total_cost = 0

    def return_invested_cost(self):
        if self.transaction_type == "deposit":
            return self.total_cost
        elif self.transaction_type == "withdraw":
            return -self.total_cost

    def return_current_cost(self):
        if self.currency == 'USD':
            return self.value_from_type(self.amount, self.fees, self.transaction_type)
        else:
            exchange_rate = get_fiat_usd_rate(self.currency)
            amount = self.amount * exchange_rate
            fees = self.fees * exchange_rate
            return self.value_from_type(amount, fees, self.transaction_type)

    @staticmethod
    def value_from_type(amount, fees, transaction_type):
        if transaction_type == 'deposit':
            return amount-fees
        elif transaction_type == 'withdraw':
            return -amount


def get_fiat_usd_rate(currency):
    exchange_rate_url = "https://ratesapi.io/api/latest?symbols=USD&base={}".format(currency)
    r = requests.get(exchange_rate_url)
    if r.status_code == 200:
        exchange_json = r.json()
        return exchange_json["rates"]["USD"]
    else:
        print("error")
        return
