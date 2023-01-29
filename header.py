import requests
import json
class decision():
    def __init__(self):
        self.market_value=0
        self.rain=0
        self.previous_price = 0
        self.switch = 0
        self.key=""
    def gather_key(self):
        f=open("setup.json")
        data=json.load(f)
        self.key = data["key"]
    def monster_price(self):
        self.gather_key()
        previous_price=0
        url = "https://twelve-data1.p.rapidapi.com/price"

        querystring = {"symbol":"MNST","format":"json","outputsize":"30"}

        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        js=response.json()
        New_price=float(js["price"])
        if New_price > previous_price:
            self.previous_price=New_price
            self.market_value=1
        if New_price < previous_price:
            self.previous_price = New_price
            self.market_value = 0

    def weather(self):
        self.gather_key()
        url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

        querystring = {"lon":"9.935932","lat":"57.046707","units":"metric","lang":"en"}

        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        js=response.json()
        rain=js["data"][0]["precip"]
        self.rain = rain
    def time(self):
        from datetime import datetime
        time_now = datetime.now().strftime("%H")
        time_now=int(time_now)
        if 8 <= time_now < 23:
            self.switch=1
            self.timer=time_now
        else:
            self.switch=0
                        
        
class wled_lightning(decision):
    def __init__(self, IP):
        super().__init__()
        self.ip = IP
        self.on = "http://{}/win&T={}&R={}&G={}%B={}&A=255&FX={}"
        self.red= 255
        self.blue=0
        self.green=0
        self.effect=0
    def blink(self):
        super().weather()
        if self.rain:
            self.effect=55
        else:
            self.effect=0

    def money(self):
        super().monster_price()
        if self.market_value:
            self.red=0
            self.green=255
            self.blue=0
        else:
            self.red=255
            self.green=0
            self.blue=0

    def send_request(self):
        self.money()
        self.blink()
        super().time()
        command=self.on.format(self.ip,str(self.switch),str(self.red),str(self.green),str(self.blue),str(self.effect))
        requests.get(command)
        