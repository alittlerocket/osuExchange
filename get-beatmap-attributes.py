from osuExchange.beatmaps import get_beatmap_attributes

access_token = open('token', 'r').read()

print(get_beatmap_attributes(access_token, 3770868))
