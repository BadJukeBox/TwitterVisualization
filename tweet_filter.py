import json
from geojson import MultiPoint as mp
import numpy as np
import matplotlib.pyplot as plt

tweets_data = []
tweets_file = open('twitter_data_sd.txt', "r", encoding='utf-16')
for line in tweets_file:
    if line.strip():
        tweet = json.loads(line)
        tweets_data.append(tweet)
notvalid = 0
valid = 0
coords = []
for n in tweets_data:
    try:
        if n['user']['geo_enabled']:
            coords.append(n['coordinates']['coordinates'])
        valid += 1
    except TypeError:
        notvalid += 1

# coords = set(map(lambda tweet_info: tweet_info['coordinates']['coordinates'], tweets_data))

print(mp(coords))

