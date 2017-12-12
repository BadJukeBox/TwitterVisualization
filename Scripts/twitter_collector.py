# Import the necessary methods from tweepy library
import linecache

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

# Variables that contains the user credentials to access Twitter API
creds = open("../credentials.txt", "r")
access_token = creds.readline().rstrip()
access_token_secret = creds.readline().rstrip()
consumer_key = creds.readline().rstrip()
consumer_secret = creds.readline()


class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
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