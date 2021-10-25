# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:06:01 2020

@author: gabriel.marin
"""

import threading
import time

import tweepy #https://github.com/tweepy/tweepy
import os

from tweepy import Stream
from tweepy import OAuthHandler


class MyListener (Stream):
    path_json = "SpydyNWH.json"

    def on_data(self, data):
        print("h")
        with open (self.path_json, 'a') as f:
            if os.path.getsize(self.path_json) > 0:
                f.write(",")
            else:
                f.write("[")
        try:
            with open(self.path_json, 'ab') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error en el dato: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True

    def on_disconnect(self):
        print("ha acabao")
        with open(self.path_json, 'a') as f:
            f.write("]")


def cerrarALos2min(stream: Stream):
    print("inicio")
    time.sleep(120)
    stream.disconnect()

#Credenciales del Twitter API
consumer_key = "0n8rRu7WcloD53DdsEBJbZIsl"
consumer_secret = "WWNvWcYJkUTS6rf6MxAAds9J9OobygankFmSi4LIggmjpF2oTw"
access_token = "930839056715603968-mKMUqgdQ7E4cO7bUJslSHRaxzkcFHYo"
access_secret = "xGlonpxh7WV0NFsusAiYxFMtLAaWI1rRHnafs6X8KHSgm"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

twitter_stream = MyListener(consumer_key, consumer_secret, access_token, access_secret)
tempo = threading.Thread(target=cerrarALos2min, args=(twitter_stream,))
tempo.start()
twitter_stream.filter(track=['#SpiderManNoWayHome'])






