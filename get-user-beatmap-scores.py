from osuExchange.scores import get_user_beatmap_scores

access_token = open("token", "r").read()

user_id = 8908337
beatmap_id = 939209

print(f'Fetching scores for user with id {user_id} on beatmap {beatmap_id}')

scores = get_user_beatmap_scores(access_token, beatmap_id,user_id)

print(f'Fetched {len(scores)} scores! Now printing a few details of each:\n')

for score in scores:
	print(f'User_ID: {score.user_id}')
	print(f'Score: {score.score}')
	print(f'Accuracy: {score.accuracy}')
	print(f'Max_Combo: {score.max_combo}\n')

