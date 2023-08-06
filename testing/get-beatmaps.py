from osuExchange.beatmaps import get_beatmaps

access_token = open("token", "r").read()

beatmap_ids = [1505967, 2276180]

print(f'Fetching beatmaps with ids {beatmap_ids}')

beatmaps = get_beatmaps(access_token, beatmap_ids)

print(f'Fetched {len(beatmaps)} beatmaps')
print('Now printing the beatmaps with a few details of each...\n')

for beatmap in beatmaps:
    print(f'Beatmap ID: {beatmap.id}')
    print(f'Beatmap tempo (BPM): {beatmap.bpm}')
    print(f'User ID of beatmap creator: {beatmap.user_id}\n')
