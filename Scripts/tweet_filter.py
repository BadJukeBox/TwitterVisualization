import json
from geojson import MultiPoint as mp
import time

tweets_data = []
tweets_file = open('../Data/twitter_data_sd.txt', "r", encoding='utf-16')
for line in tweets_file:
    if line.strip():
        tweet = json.loads(line)
        tweets_data.append(tweet)
notvalid = 0
valid = 0
coords = []


# Bound box for San Diego
lborder = -117.3332977295
rborder = -117.067
tborder = 32.8403
bborder = 32.6996

for n in tweets_data:
    try:
        if n['user']['geo_enabled']:
            print(repr(n['created_at']))
            print(time.strftime('%H:%M:%S', time.strptime(n['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))
            coord = n['coordinates']['coordinates']
            if lborder <= coord[0] <= rborder and bborder <= coord[1] <= tborder:
                coords.append(n['coordinates']['coordinates'])

        valid += 1
    except TypeError:
        notvalid += 1


# coords = set(map(lambda tweet_info: tweet_info['coordinates']['coordinates'], tweets_data))

print(mp(coords))


