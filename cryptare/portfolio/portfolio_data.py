import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from diskcache import Cache
from diskcache import Index

from cryptare.portfolio.User import User

if not len(firebase_admin._apps):
    cred = credentials.Certificate('../../service_account_info/Cryptare-9d04b184ba96.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://atalwcryptare.firebaseio.com/'
    })
else:
    firebase_admin.get_app()
ref = db.reference()

cache = Cache('/tmp/portfolios_cache')
cache_store_time = 60*60*12

users = []

def get_user_data():
    cache.expire()
    key = 'portfolios'
    index = Index.fromcache(cache)

    if key in index:
        print('in cache')
        return dict(index[key])
    else:
        all_data = ref.child(key).get()
        cache.set(key, all_data, expire=cache_store_time)
        return all_data


def extract_user_data():
    all_data = get_user_data()
    for user_id, data in all_data.items():
        if 'CryptoData' in data:
            crypto_data = data['CryptoData']
        else:
            crypto_data = {}

        if 'FiatData' in data:
            fiat_data = data['FiatData']
        else:
            fiat_data = {}

        if 'Names' in data:
            names = data['Names']
        else:
            continue

        users.append(User(user_id, crypto_data, fiat_data, names))


extract_user_data()