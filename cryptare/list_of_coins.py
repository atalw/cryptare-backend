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
storage = firebase.storage()

def update_list_of_coins_with_rank():
    url = "https://api.coinmarketcap.com/v1/ticker/?limit=50"
    r = requests.get(url)
    dict = {}
    if r.status_code == 200:
        json = r.json()
        for index in range(len(json)):
            symbol = json[index]["symbol"]
            if symbol == "MIOTA":
                symbol = "IOT"
            elif symbol == "NANO":
                symbol = "XRB"

            icon_url = storage.child("icons/{}.png".format(symbol.lower())).get_url()
            dict[symbol] = {}
            dict[symbol]["rank"] = float(json[index]["rank"])
            dict[symbol]["name"] = json[index]["name"]
            if icon_url is not None:
                dict[symbol]["icon_url"] = icon_url

        title = "coins"
        db.child(title).push(dict)
    else:
        return "list coin error"

update_list_of_coins_with_rank()