import requests
import pyrebase
import time

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

coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
currencies = ["INR", "USD", "GBP", "JPY", "CNY", "SGD", "EUR", "ZAR"]

def update_current_bitcoin_price():
    for currency in currencies:
        price = get_current_bitcoin_price(currency)
        if price is not None:
            # store price and timestamp
            data = {"timestamp": time.time(), "price": price}
            title = "current_btc_price_{}".format(currency)
            db.child(title).push(data)
        else:
            print("current btc error")



def get_current_bitcoin_price(currency):
    url = "https://api.coindesk.com/v1/bpi/currentprice/{}.json".format(currency)
    r = requests.get(url)
    if r.status_code == 200:
        json = r.json()
        price = json["bpi"][currency]["rate_float"]
        return price
    return None