from osuExchange.auth import get_access_token, OAuth2Scope
from json import JSONDecoder

# Open and read client_info.json
client_info_str = open('client_info.json', 'r').read()

# Parse the JSON to construct a dict of the properties of the osu! client
# client_id: str, client_secret: str,  redirect_uri: str are the only attributes you need.
client_info: dict[str, str] = JSONDecoder().decode(client_info_str)

# Define the necessary OAuth2 scopes
scopes = [
    OAuth2Scope.PUBLIC,
    OAuth2Scope.IDENTIFY
]

# Get a user access token on behalf of user currently logged in on their browser
access_token_obj = get_access_token(**client_info, scopes=scopes)

# Save the raw token to a file
open('token', 'w').write(access_token_obj.access_token)
