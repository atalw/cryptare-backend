from cryptare.portfolio.Transaction import Crypto_Transaction

class Portfolio:

    def __init__(self, name, crypto_data, fiat_data):
        self.name = name
        self.crypto_data = crypto_data
        self.fiat_data = fiat_data
        self.crypto_transactions = []
        self.fiat_transactions = []

        self.create_crypto_transactions()

    def create_crypto_transactions(self):
        # print(self.crypto_data)
        for coin, transaction_list in self.crypto_data.items():
            print(transaction_list)
            for transaction in transaction_list:
                if 'type' in transaction:
                    transaction_type = transaction['type']
                else:
                    continue

                if 'coin' in transaction:
                    coin = transaction['coin']
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

                if 'totalCost' in transaction:
                    total_cost = transaction['totalCost']
                else:
                    continue

                self.crypto_transactions.append(Crypto_Transaction(transaction_type, coin, trading_pair, exchange, cost_per_coin, amountOfCoins, fees, total_cost))

        # self.calculate_total_invested()

        self.calculate_current_value()



    def calculate_total_invested(self):
        total = 0
        for transaction in self.crypto_transactions:
            total += transaction.return_invested_cost()

        print(total)

    def calculate_current_value(self):
        total = 0
        for transaction in self.crypto_transactions:
            total += transaction.return_current_cost()

        print(total)