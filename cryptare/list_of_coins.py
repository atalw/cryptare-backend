import requests
import pyrebase

config = {
    "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
    "authDomain": "atalwcryptare.firebaseapp.com",
    "databaseURL": "https://atalwcryptare.firebaseio.com/",
    "storageBucket": "atalwcryptare.appspot.com",
    "serviceAccount": "../service_account_info/Cryptare-9d04b184ba96.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def update_list_of_coins_with_rank():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=50"
    r = requests.get(url)
    dict = {}
    if r.status_code == 200:
        json = r.json()
        for index in range(len(json)):
            symbol = json[index]["symbol"]
            dict[symbol] = {}
            dict[symbol]["rank"] = float(json[index]["rank"])
            dict[symbol]["name"] = json[index]["name"]

        title = "coins"
        db.child(title).push(dict)
    else:
        return "list coin error"

update_list_of_coins_with_rank()