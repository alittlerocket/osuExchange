from osuExchange.scores import get_score

access_token = open("token", "r").read()

score_id = 3142585620

print(f'Fetching score from score_id {score_id}')

#Not sure how to do this one
score = get_score(access_token, mode='osu', score_id)

print('Fetched score! Now printing a few of its details...\n')

print(f'Fetched {len(score.scores)} score')

for all in score.scores:
    print(f'User id: {all.user_id}')
    print(f'Score: {all.score}')
    print(f'PP: {all.pp}')
    print(f'Rank: {all.rank}')
    print(f'Accuracy: {all.accuracy}')
