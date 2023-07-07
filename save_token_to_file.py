from auth import get_access_token, OAuth2Scope
from json import JSONDecoder

client_info = JSONDecoder().decode(open('client_info.json', 'r').read())

scopes=[OAuth2Scope.PUBLIC, OAuth2Scope.IDENTIFY]

access_token_obj = get_access_token(**client_info, scopes=scopes)

open('token.txt', 'w').write(access_token_obj.access_token)
