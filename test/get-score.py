from osuExchange.scores import get_score

access_token = open("token", "r").read()

score_id = 3142585620

print(f'Fetching the from score_id {score_id}')

#Not sure how to do this one
score = get_score(access_token, 'osu', score_id)

print('Fetched score! Now printing a few of its details...\n')

print(f'Fetched {score.score} score')
print(f'Fetched {score.pp}')

if (score.user != None):
    print(f'Fetched {score.user.username}')


