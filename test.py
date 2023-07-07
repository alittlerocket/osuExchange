from beatmap import get_beatmap_attributes, get_beatmap

access_token = open("token.txt").read()

print(get_beatmap(access_token, 658127).bpm)

