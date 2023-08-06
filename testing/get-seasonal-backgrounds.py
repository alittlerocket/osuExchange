from osuExchange.seasonalbg import get_seasonal_backgrounds

access_token = open("token", "r").read()

user_id = 8908337
beatmap_id = 939209

print(f'Fetching scores for user with id {user_id} on beatmap {beatmap_id}')

bgs = get_seasonal_backgrounds(access_token)

print(f"A link to a Seasonal Background: {bgs.backgrounds[1].url}")