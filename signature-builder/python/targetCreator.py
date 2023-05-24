import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests

public_key = "14b4b6dad69204031babe97a198447c0cac11cd26b688cf1811273d76ce7a100"
secret_key = "720d6bacaf70b95d7fb29b67a6ca2e4ac36f65804febb29195cbdb55dd7393f414b4b6dad69204031babe97a198447c0cac11cd26b688cf1811273d76ce7a100"
class User():
    def __init__(self, public_key, private_key) -> None:
        pass
        # replace with api keys
        self.public_key = public_key
        self.secret_key = private_key
        # change url to prod
        self.rootApiUrl = "https://api.dmarket.com"


    def get_offer_from_market(self):
        market_response = requests.get(self.rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit=1&currency=USD")
        offers = json.loads(market_response.text)["objects"]
        return offers[0]
    
    def get_account_info(self) -> requests.models.Response:
        return self.Call_API("GET", "/account/v1/user")
    
    def get_account_balance(self) -> requests.models.Response:
        return self.Call_API("GET", "/account/v1/balance")

    def deposit_items(self):
        pass

    def deposit_status(self):
        pass

    def get_user_offers(self) -> requests.models.Response:
        return self.Call_API("GET", "/marketplace-api/v1/user-offers")
    
    def get_user_inventory(self) -> requests.models.Response:
        return self.Call_API("GET", "/marketplace-api/v1/user-inventory")
    
    def get_user_items(self) -> requests.models.Response:
        return self.Call_API("GET", "/exchange/v1/user/items")

    #Still don't know what this does.
    def build_target_body_from_offer(offer):
        return {"targets": [
            {"amount": 1, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
            "attributes": {"gameId": offer["gameId"],
                            "categoryPath": offer["extra"]["categoryPath"],
                            "title": offer["title"],
                            "name": offer["title"],
                            "image": offer["image"],
                            "ownerGets": {"amount": "1", "currency": "USD"}}}
        ]}

    def GetTimeStamp(self) -> str:
        return str(round(datetime.now().timestamp()))
    
    def Call_API(self, method : str, api_request_path : str) -> requests.models.Response:
        body = self.rootApiUrl + api_request_path
        string_to_sign = method + api_request_path + json.dumps(body) + self.GetTimeStamp()
        signature_prefix = "dmar ed25519 "
        encoded = string_to_sign.encode('utf-8')
        secret_bytes = bytes.fromhex(secret_key)
        signature_bytes = crypto_sign(encoded, secret_bytes)
        signature = signature_bytes[:64].hex()
        headers = {
            "X-Api-Key": public_key,
            "X-Request-Sign": signature_prefix + signature,
            "X-Sign-Date": self.GetTimeStamp()
        }
        if method == "GET":
            resp = requests.get(self.rootApiUrl + api_request_path, json=body, headers=headers)
        elif method == "POST":
            resp = requests.post(self.rootApiUrl + api_request_path, json=body, headers=headers)
        return resp

if __name__ == "__main__":
    Me = User(public_key=public_key, private_key=secret_key)
    resp = Me.get_user_inventory()
    """stuff = resp.json()
    for item in stuff["Items"]:
        title = item["Title"]
        withdrawable = item["Withdrawable"]
        depositable = item["Depositable"]
        print(f"{title} : {depositable}")"""