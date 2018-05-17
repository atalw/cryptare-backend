from cryptare.portfolio.Portfolio import Portfolio


class User:

    def __init__(self, user_id, crypto_data, fiat_data, names):
        self.user_id = user_id
        self.crypto_data = crypto_data
        self.fiat_data = fiat_data
        self.names = names
        self.portfolios = []
        self.create_portfolios()

    def create_portfolios(self):
        for name in self.names:
            if name in self.crypto_data:
                portfolio_crypto_data = self.crypto_data[name]
            else:
                portfolio_crypto_data = {}

            if name in self.fiat_data:
                portfolio_fiat_data = self.fiat_data[name]
            else:
                portfolio_fiat_data = {}

            self.portfolios.append(Portfolio(self.user_id, name, portfolio_crypto_data, portfolio_fiat_data))