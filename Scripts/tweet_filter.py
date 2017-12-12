import json
from geojson import MultiPoint as mp
import time

tweets_data = []
tweets_file = open('../Data/twitter_data.txt', "r", encoding='utf-16')
for line in tweets_file:
    if line.strip():
        tweet = json.loads(line)
        tweets_data.append(tweet)

# Bound box for San Diego
lborder = -117.3332977295
rborder = -117.067
tborder = 32.8403
bborder = 32.6996

invalid = valid = 0
times = {}
for n in tweets_data:
    try:
        if n['coordinates'] is not None:
            valid += 1
            hour = time.strftime('%H', time.strptime(n['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            coord = n['coordinates']['coordinates']
            if lborder <= coord[0] <= rborder and bborder <= coord[1] <= tborder:
                times.setdefault(hour, []).append(coord)

    except TypeError as e:
        print('invalid tweet' + str(n) + e)
        invalid += 1

leng = 0
for key, value in times.items():
    print(len(value))
    leng += len(value)
    print(leng)
print(len(tweets_data))
print(leng)
print(valid)
print(invalid)
# coords = set(map(lambda tweet_info: tweet_info['coordinates']['coordinates'], tweets_data))

# print(mp(coords))


