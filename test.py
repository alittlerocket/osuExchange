from beatmap import get_beatmap_attributes, get_beatmap
from ossapi import Ossapi

# client_id = 22257
# client_secret = "2uF9ngKYzYrrVdApOUStH2e8er73a9cbZpZrsbUw"
# api = Ossapi(client_id, client_secret)

# beatmap = api.beatmap(658127)
# print(beatmap.bpm)

access_token = open("token.txt").read()

print(get_beatmap(access_token, 658127).bpm)

