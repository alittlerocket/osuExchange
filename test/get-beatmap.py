from osuExchange.beatmaps import get_beatmap

access_token = open("token", "r").read()

beatmap_id = 100608

print(f'Fetching beatmap with id {beatmap_id}')

beatmap = get_beatmap(access_token, beatmap_id)

print('Fetched beatmap! Now printing a few of its details...\n')

print(f'ID: {beatmap.id}')
print(f'Approach Rate: {beatmap.approach_rate}')
print(f'Beatmapset ID: {beatmap.beatmapset_id}')
