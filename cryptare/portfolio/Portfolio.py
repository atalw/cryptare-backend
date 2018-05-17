import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from Transaction import CryptoTransaction
from Transaction import FiatTransaction

import time


class Portfolio:

    if not len(firebase_admin._apps):
        cred = credentials.Certificate('../../service_account_info/Cryptare-9d04b184ba96.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://atalwcryptare.firebaseio.com/'
        })
    else:
        firebase_admin.get_app()

    ref = db.reference()

    def __init__(self, user_id, name, crypto_data, fiat_data):
        self.user_id = user_id
        self.name = name
        self.crypto_data = crypto_data
        self.fiat_data = fiat_data
        self.crypto_transactions = []
        self.fiat_transactions = []

        self.create_crypto_transactions()
        self.create_fiat_transactions()

        if len(fiat_data) == 0 and len(crypto_data) == 0:
            return

        self.calculate_total_invested()
        self.calculate_current_value()

    def create_crypto_transactions(self):
        for coin, transaction_list in self.crypto_data.items():
            for transaction in transaction_list:
                if 'type' in transaction:
                    transaction_type = transaction['type']
                else:
                    continue

                if 'tradingPair' in transaction:
                    trading_pair = transaction['tradingPair']
                else:
                    continue

                if 'exchange' in transaction:
                    exchange = transaction['exchange']
                else:
                    continue

                if 'exchangeDbTitle' in transaction:
                    exchange_db_title = transaction['exchangeDbTitle']
                else:
                    continue

                if 'costPerCoin' in transaction:
                    cost_per_coin = transaction['costPerCoin']
                else:
                    continue

                if 'amountOfCoins' in transaction:
                    amountOfCoins = transaction['amountOfCoins']
                else:
                    continue

                if 'fees' in transaction:
                    fees = transaction['fees']
                else:
                    continue

                if 'totalCostUsd' in transaction:
                    total_cost_usd = transaction['totalCostUsd']
                else:
                    continue

                if transaction_type == 'cryptoBuy':
                    self.crypto_transactions.append(
                        CryptoTransaction(transaction_type, coin, "USD", exchange_db_title, amountOfCoins, fees,
                                           total_cost_usd))
                else:
                    self.crypto_transactions.append(CryptoTransaction(transaction_type, coin, trading_pair,
                                                                      exchange_db_title, amountOfCoins,
                                                                      fees, total_cost_usd))

    def create_fiat_transactions(self):
        for currency, transaction_list in self.fiat_data.items():
            for transaction in transaction_list:
                if 'type' in transaction:
                    transaction_type = transaction['type']
                else:
                    continue

                if 'amount' in transaction:
                    amount = transaction['amount']
                else:
                    continue

                if 'fees' in transaction:
                    fees = transaction['fees']
                else:
                    continue

                self.fiat_transactions.append(FiatTransaction(transaction_type, currency, amount, fees))

    def calculate_total_invested(self):
        total = 0
        for transaction in self.crypto_transactions:
            total += transaction.return_invested_cost()

        self.total_invested = total
        self.ref.child('portfolios').child(self.user_id).child('totalInvested').child(self.name).push({
            'timestamp': time.time(),
            'price': total
        })

    def calculate_current_value(self):
        total = 0
        for transaction in self.crypto_transactions:
            total += transaction.return_current_cost()

        for transaction in self.fiat_transactions:
            total += transaction.return_current_cost()

        self.total_current_value = total
        self.ref.child('portfolios').child(self.user_id).child('totalCurrentValue').child(self.name).push({
            'timestamp': time.time(),
            'price': total
        })