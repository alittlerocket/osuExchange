from osuExchange.users import get_users

access_token = open("token", "r").read()

user_ids = [10652591, 12625512]

print(f'Fetching users with ids {user_ids}')

users = get_users(access_token, user_ids)

print(f'Fetched {len(users)} users! Now printing a few details of each:\n')

for user in users:
	print(f'User ID: {user.id}')
	print(f'User name: {user.username}')
	print(f'User country code: {user.country_code}')
	print(f'Last visit: {user.last_visit}')
	print()
