from osuExchange.scores import get_beatmap_scores

access_token = open("token", "r").read()

beatmap_id = 126645

print(f'Fetching beatmap scores for beatmap with id {beatmap_id}')

beatmap_scores = get_beatmap_scores(access_token, beatmap_id)

print('Fetched beatmap scores! Now printing a few of its details...\n')

print(f'Fetched {len(beatmap_scores.scores)} scores for {beatmap_id}')

for score in beatmap_scores.scores:
    print(f'User_ID: {score.user_id}')
    print(f'Score: {score.score}')
    print(f'Accuracy: {score.accuracy}')
    print(f'Max_Combo: {score.max_combo}\n')
