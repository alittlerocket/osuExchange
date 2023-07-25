from osuExchange.scores import download_score

access_token = open("token", "r").read()

score_id = 3142585620

print(f'Fetching score from score_id {score_id}')

#Not sure how to do this one
download_s = download_score(access_token, mode='osu', score_id, True)

print('Fetched download_score! Now printing a few of its details...\n')

print(f'Fetched {len(download_s.scores)} score')

for all in download_s.scores:
    print(f'User: {all.user}')
    print(f'Beatmap: {all.beatmap}')
