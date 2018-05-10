# import logging
# logging.basicConfig(level=logging.DEBUG)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from concurrent.futures import ThreadPoolExecutor
import ccxt
from itertools import islice

from diskcache import Cache
from diskcache import Index

cred = credentials.Certificate('../service_account_info/Cryptare-9d04b184ba96.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://atalwcryptare.firebaseio.com/',
})

# As an admin, the app has access to read and write all data, regardless of Security Rules
ref = db.reference()

cache = Cache('/tmp/coin_alerts_users_cache')
cache_store_time = 60*30

coins = ["BTC", "ETH", "LTC", "BCH", "XRP", "NEO", "GAS", "XLM", "DASH", "OMG",
         "QTUM", "REQ", "ZRX", "GNT", "BAT", "AE", "RPX", "DBC", "XMR", "DOGE",
         "SIA", "TRX", "DGB", "ZEC", "BTG", "IOT", "ZIL", "ETN", "ONT", "KNC",
         "EOS", "POLY", "AION", "NCASH", "ICX", "VEN"]

currencies = ["INR", "USD", "GBP", "CAD", "JPY", "CNY", "SGD", "EUR", "ZAR", "AUD"]

all_markets = {}
all_exchange_update_type = {}

all_exchange_prices = {}
all_market_data = {}

coin_alerts_users_dict = {}
coin_alerts_users_exchanges = []


def update_ccxt_market_price_alt(market, market_name, market_database_title):
    # print('here', market)

    # market.pro
    # print(market.has)
    data_dict = {}

    if 'fetchTickers' in market.has:
        if market.has['fetchTickers']:
            market_tickers = market.fetch_tickers()
        else:
            market_tickers = {}
    else:
        market_tickers = {}

    market_markets = {}
    if 'loadMarkets' in market.has:
        # print('fals')
        if market.has['loadMarkets']:
            market_markets = market.load_markets()
    elif 'fetchMarkets' in market.has:
        if market.has['fetchMarkets']:
            market_markets = market.fetch_markets()
            # print(market_markets)

    if isinstance(market_markets, dict):
        # print('its a dict')
        for symbol, value in market_markets.items():
            coin = value['base']
            coin_pair = value['quote']
            if coin not in data_dict:
                data_dict[coin] = {}
            if coin_pair not in data_dict[coin]:
                data_dict[coin][coin_pair] = {}
    elif isinstance(market_markets, list):
        # print('its not a dict')
        for symbol in market_markets:
            coin = symbol['base']
            coin_pair = symbol['quote']
            if coin not in data_dict:
                data_dict[coin] = {}
            if coin_pair not in data_dict[coin]:
                data_dict[coin][coin_pair] = {}

    # print(market_tickers)
    # print(data_dict)
    for coin, coin_pairs in data_dict.items():
        for coin_pair in coin_pairs:
            symbol = "{0}/{1}".format(coin, coin_pair)
            if symbol in market_tickers:
                info = market_tickers[symbol]
            else:
                # print(symbol)
                info = market.fetch_ticker(symbol)
            try:
                data_dict[coin][coin_pair]['buy_price'] = string_to_float(info['ask'])
                data_dict[coin][coin_pair]['sell_price'] = string_to_float(info['bid'])
                data_dict[coin][coin_pair]['last_price'] = string_to_float(info['last'])
                data_dict[coin][coin_pair]['max_24hrs'] = string_to_float(info['high'])
                data_dict[coin][coin_pair]['min_24hrs'] = string_to_float(info['low'])
                data_dict[coin][coin_pair]['vol_24hrs'] = string_to_float(info['baseVolume'])
            except:
                continue
    # print(data_dict)
    for coin, coin_pairs in data_dict.items():
        for coin_pair in coin_pairs:
            all_market_data["{0}/{1}/{2}".format(market_database_title, coin, coin_pair)] = data_dict[coin][coin_pair]
            add_market_entry(coin, coin_pair, '{}'.format(market_name), '{}'.format(market_database_title))
            update_coin_alerts_uids(market_name, coin, coin_pair, data_dict[coin][coin_pair]['buy_price'])
    all_exchange_update_type['{}'.format(market_name)] = 'update'




def string_to_float(value):
    if value is not None:
        return float(value)
    else:
        return 0

def get_coin_alerts_users():
    cache.expire()

    global coin_alerts_users_dict
    key = 'coin_alerts_users'
    index = Index.fromcache(cache)
    if key in index:
        # coin_alerts_users_dict = dict(index[key])
        coin_alerts_users_dict = {} # populate dict every x minutes and write to alerts with a 15 minute delay
    else:
        result = ref.child(key).get()
        cache.set(key, result, expire=cache_store_time)
        coin_alerts_users_dict = dict(result)


def get_coin_alerts_uids(market_name, coin, pair):
    if market_name in coin_alerts_users_dict:
        result = coin_alerts_users_dict[market_name]
        if coin in result:
            if pair in result[coin]:
                return True, result[coin][pair]
    return False, {}


def update_coin_alerts_uids(market_name, coin, pair, price):
    (is_present, uid_data) = get_coin_alerts_uids(market_name, coin, pair)
    if is_present:
        for uid, index in uid_data.items():
            for count in range(index):
                title = 'coin_alerts/{0}/{1}/{2}/{3}/{4}/current_price'.format(uid, market_name, coin, pair, count)
                all_market_data[title] = price

###################################################

def add_market_price(coin, currency, market_name, price):
    if coin not in all_exchange_prices:
        all_exchange_prices[coin] = {}

    if currency not in all_exchange_prices[coin]:
        all_exchange_prices[coin][currency] = {}

    all_exchange_prices[coin][currency][market_name] = price


def add_market_entry(coin, currency, market_name, market_title):
    if coin not in all_markets:
        all_markets[coin] = {}

    if currency not in all_markets[coin]:
        all_markets[coin][currency] = {}

    if market_name == "Quoinex" and currency == "INR":
        pass
    else:
        # all_markets[coin][currency][market_name] = '{0}/{1}/{2}'.format(market_title, coin, currency)
        all_market_data[ "{0}/Data/{1}/markets/{2}".format(coin, currency, market_name)] = '{0}/{1}/{2}'.format(market_title, coin, currency)


def update_markets():
    for coin, values in all_markets.items():
        for currency, markets in values.items():
            title = "{0}/Data/{1}/markets".format(coin, currency)
            all_market_data[title] = markets


def update_exchange_update_type():
    """Store type of update method used for exchange data in Firebase - 'push' or 'update' """
    # ref.child("all_exchanges_update_type").update(all_exchange_update_type)
    pass


def update_all_market_data():
    for item in dict_chunks(all_market_data, 500):
        ref.update(item)


def dict_chunks(data, SIZE=500):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


with ThreadPoolExecutor() as executor:
    executor.submit(update_ccxt_market_price_alt, ccxt.coinegg(), 'CoinEgg', 'coinegg')
    executor.submit(update_ccxt_market_price_alt, ccxt.coinfloor(), 'Coinfloor', 'coinfloor')
    executor.submit(update_ccxt_market_price_alt, ccxt.ccex(), 'CCEX', 'ccex')
    executor.submit(update_ccxt_market_price_alt, ccxt.bitflyer(), 'bitFlyer', 'bitflyer')
    executor.submit(update_ccxt_market_price_alt, ccxt.bitbay(), 'BitBay', 'bitbay')
    executor.submit(update_ccxt_market_price_alt, ccxt.gatecoin(), 'BitBay', 'bitbay')
    executor.submit(update_ccxt_market_price_alt, ccxt.independentreserve(), 'gatecoin', 'gatecoin')
    executor.submit(update_ccxt_market_price_alt, ccxt.gdax(), 'GDAX', 'gdax')
    executor.submit(update_ccxt_market_price_alt, ccxt.okex(), 'OKEX', 'okex')
    executor.submit(update_ccxt_market_price_alt, ccxt.itbit(), 'itBit', 'itbit')
    executor.submit(update_ccxt_market_price_alt, ccxt.bibox(), 'Bibox', 'bibox')
    executor.submit(update_ccxt_market_price_alt, ccxt.mixcoins(), 'mixcoins', 'mixcoins')
    executor.submit(update_ccxt_market_price_alt, ccxt.coinmate(), 'CoinMate', 'coinmate')
    executor.submit(update_ccxt_market_price_alt, ccxt.bitlish(), 'Bitlish', 'bitlish')
    executor.submit(update_ccxt_market_price_alt, ccxt.vaultoro(), 'Vaultoro', 'vaultoro')
    executor.submit(update_ccxt_market_price_alt, ccxt.fybsg(), 'FYBSG', 'fybsg')
    executor.submit(update_ccxt_market_price_alt, ccxt.vbtc(), 'VBTC', 'vbtc')
    executor.submit(update_ccxt_market_price_alt, ccxt.surbitcoin(), 'SurBitcoin', 'surbitcoin')
    executor.submit(update_ccxt_market_price_alt, ccxt.btctradeua(), 'BTCTradeUA', 'btctradeua')
    executor.submit(update_ccxt_market_price_alt, ccxt.btcmarkets(), 'BTCMarkets', 'btcmarkets')
    executor.submit(update_ccxt_market_price_alt, ccxt.virwox(), 'VirWoX', 'virwox')
    executor.submit(update_ccxt_market_price_alt, ccxt.quadrigacx(), 'QuadrigaCX', 'quadrigacx')
    executor.submit(update_ccxt_market_price_alt, ccxt.bl3p(), 'Blep', 'blep')
    executor.submit(update_ccxt_market_price_alt, ccxt.paymium(), 'Paymium', 'paymium')


# update_markets()
update_exchange_update_type()
update_all_market_data()