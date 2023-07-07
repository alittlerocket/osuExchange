from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import post
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open as open_browser
from exception import OsuApiException
from enum import Enum

class OAuth2Scope(Enum):
	CHAT_WRITE = 'chat.write'
	DELEGATE = 'delegate'
	FORUM_WRITE = 'forum.write'
	FRIENDS_READ = 'friends.read'
	IDENTIFY = 'identify'
	PUBLIC = 'public'

class OsuClientCredentialsToken:
	def __init__(self, json: dict):
		self.access_token: str = json['access_token']
		self.expires_in_sec: int = json['expires_in']
		self.token_type: str = json['token_type']

class OsuAccessToken(OsuClientCredentialsToken):
	def __init__(self, json: dict):
		super().__init__(json)
		self.refresh_token: str = json['refresh_token']

POST_HEADERS = {
	'Accept': 'application/json',
	'Content-Type': 'application/x-www-form-urlencoded'
}

# https://osu.ppy.sh/docs/index.html#authorization-code-grant
def get_access_token(
		client_id: str,
		client_secret: str,
		redirect_uri: str,
		scopes: list[OAuth2Scope],
		fail_message: str = 'User did not authorize the osu! client',
		success_message: str = 'User has authorized the osu! client'
	) -> OsuAccessToken:

	authorization_code: str | None = None

	class CodeHandler(BaseHTTPRequestHandler):
		# Override log_message to suppress printing to stdout
		def log_message(self, format, *args):
			pass

		# Handle Chrome's /favicon.ico request (?)
		def do_OPTIONS(self):
			self.send_response(200)
			self.send_header('Access-Control-Allow-Origin', '*')
			self.send_header('Access-Control-Allow-Methods', 'GET, POST')
			self.send_header('Access-Control-Allow-Headers', 'Content-Type')
			self.end_headers()

		# Handle osu!api's GET request containing the authorization code
		def do_GET(self):
			code = parse_qs(urlparse(self.path).query).get('code', [''])[0]
			if code == '':
				return
			if code == 'access_denied':
				self.send_error(401, fail_message)
				return
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.end_headers()
			self.wfile.write(success_message.encode())
			nonlocal authorization_code
			authorization_code = code

	# Params to identify the application and redirect the user to us
	query_params = {
		'client_id': client_id,
		'redirect_uri': redirect_uri,
		'response_type': 'code',
		'scope': ' '.join(map(lambda s: s.value, scopes)),
		'state': 'randomval'
	}

	# Open the user's browser to osu!'s authorization page
	open_browser(f'https://osu.ppy.sh/oauth/authorize/?{urlencode(query_params)}')

	url_obj = urlparse(redirect_uri)
	port: int | None = url_obj.port

	if port is None:
		port = 8080

	# Wait for the GET request containing the authorization code
	HTTPServer(('', port), CodeHandler).handle_request()

	if authorization_code is None:
		raise Exception('No authentication code received!')

	# POST the code back to get an access token
	body_params = {
		'code': authorization_code,
		'client_id': client_id,
		'client_secret': client_secret,
		'redirect_uri': redirect_uri,
		'grant_type': 'authorization_code'
	}

	resp = post(url='https://osu.ppy.sh/oauth/token', data=body_params, headers=POST_HEADERS)

	if resp.status_code >= 400:
		raise OsuApiException(resp)
	
	return OsuAccessToken(resp.json())

def refresh_access_token(
		client_id: str,
		client_secret: str,
		refresh_token: str,
		scopes: list[OAuth2Scope]
	) -> OsuAccessToken:

	body_params = {
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'refresh_token',
		'refresh_token': refresh_token,
		'scopes': ' '.join(map(lambda s: s.value, scopes))
	}

	resp = post('https://osu.ppy.sh/oauth/token', data=body_params, headers=POST_HEADERS)

	if resp.status_code >= 400:
		raise OsuApiException(resp)
	
	return OsuAccessToken(resp.json())

# https://osu.ppy.sh/docs/#client-credentials-grant
def get_client_credentials_token(client_id: str, client_secret: str) -> OsuClientCredentialsToken:
	body_params = {
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'client_credentials',
		'scope': 'public identify'
	}

	resp = post('https://osu.ppy.sh/oauth/token', data=body_params, headers=POST_HEADERS)

	if resp.status_code >= 400:
		raise OsuApiException(resp)

	return OsuClientCredentialsToken(resp.json())