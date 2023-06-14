from auth import get_access_token, OAuth2Scope
from json import JSONDecoder

client_info = JSONDecoder().decode(open('client_info.json', 'r').read())

access_token_obj = get_access_token(**client_info, scopes=[OAuth2Scope.PUBLIC])

open('token', 'w').write(access_token_obj.access_token)
