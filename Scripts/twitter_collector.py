# Import the necessary methods from tweepy library
import linecache

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sqlite3
import json
from geojson import Feature, FeatureCollection, Point, dump
import time

# Variables that contains the user credentials to access Twitter API
creds = open("../credentials.txt", "r")
access_token = creds.readline().rstrip()
access_token_secret = creds.readline().rstrip()
consumer_key = creds.readline().rstrip()
consumer_secret = creds.readline()

lborder = -117.3332977295
rborder = -117.067
tborder = 32.8403
bborder = 32.6996

writeCon = sqlite3.connect('tweets.db')
writeCursor = writeCon.cursor()
writeCursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets(hour INTEGER, latitude TEXT, longitude TEXT)
''')
writeCon.commit()


def filter_by_hour(tweet):
    try:
        if tweet['coordinates'] is not None:
            hour = time.strftime('%H', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            coord = tweet['coordinates']['coordinates']
            if lborder <= coord[0] <= rborder and bborder <= coord[1] <= tborder:
                tweet['created_at'] = hour
                return [hour, coord[0], coord[1]]
            else:
                return None
        else:
            return None

    except TypeError as e:
        print('invalid tweet' + str(tweet) + e)


class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = filter_by_hour(json.loads(data))
        if tweet is not None:
            writeCursor.execute('''INSERT INTO tweets(hour, latitude, longitude)
                              VALUES(?,?,?)''', (tweet[0], tweet[1], tweet[2]))
            writeCon.commit()
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, wait_on_rate_limit=True)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(locations=[-117.3332977295, 32.5552055163, -116.9487762451, 32.9525038812])