# Simple Twitter bot that retrieves Bitcoin price information and tweets it out, every 5 minutes.

import tweepy
import json
import requests
import sched, time

import keys

class TwitterBot:

    # keys contained in separate file
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    access_token = keys.access_token
    access_token_secret = keys.access_token_secret

    api = tweepy.API()
    api_url = "https://api.cryptonator.com/api/ticker/btc-usd"
    message = ""

    s = sched.scheduler(time.time, time.sleep)

     def __init__(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        user = self.api.me()
        print(user.name)

        # schedule event to run in 5 minutes
        self.s.enter(300, 1, self.send_update)
        self.s.run()

    def send_update(self):
        self.get_price_data()
        self.tweet(self.message)
        self.s.enter(300, 1, self.send_update)  # reschedule event

    def get_price_data(self):
        response = requests.get(self.api_url)
        bitcoin_data = json.loads(response.text)
        bitcoin_data = bitcoin_data["ticker"]
        base = bitcoin_data["base"]
        target = bitcoin_data["target"]
        price = float(bitcoin_data["price"])
        volume = float(bitcoin_data["volume"])
        self.message = f'{base}-{target}: ${price:.2f}\nVolume: {volume:.2f} BTC'

    def tweet(self, message):
        self.api.update_status(message)


twit = TwitterBot()