from osuExchange.beatmaps import get_beatmap_attributes

access_token = open("token", "r").read()

beatmap_id = 1414258

print(f'Fetching beatmaps with id {beatmap_id}')

beatmap = get_beatmap_attributes(access_token, beatmap_id)

print('Now printing the beatmaps with a few details of each...\n')

print(f'Beatmap ID: {beatmap.approach_rate}')
print(f'Beatmap ID: {beatmap.max_combo}')
print(f'Beatmap ID: {beatmap.star_rating}')