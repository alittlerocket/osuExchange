# https://osu.ppy.sh/docs/index.html#authorization-code-grant
# Read this

from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import post
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open as open_browser

class OsuAuthenticationException(BaseException):
	def __init__(self, message: str):
		super().__init__(message)

class OAuth2AccessToken:
	def __init__(self, json: dict):
		self.access_token: str = json['access_token']
		self.expires_in: str = json['expires_in']
		self.refresh_token: str = json['refresh_token']
		self.token_type: str = json['token_type']

def get_access_token(client_id: str, client_secret: str, redirect_uri: str, port: int) -> OAuth2AccessToken:
	# Unforunately, this is the best way to keep `authorization_code` and `CodeHandler` inaccessible by other modules

	authorization_code: str | None = None

	class CodeHandler(BaseHTTPRequestHandler):
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
				self.send_error(401, 'You did not authorize the osu! application.')
				return
			self.send_response(200)
			self.wfile.write(b'You have authorized the osu! application. You may now close this tab.')
			nonlocal authorization_code
			authorization_code = code

	# Params to identify the application and redirect the user to us
	params = {
		'client_id': client_id,
		'redirect_uri': redirect_uri,
		'response_type': 'code',
		'scope': 'public identify',
		'state': 'randomval'
	}

	# Open the user's browser to osu!'s authorization page
	open_browser(f'https://osu.ppy.sh/oauth/authorize/?{urlencode(params)}')

	# Wait for the GET request containing the authorization code
	HTTPServer(('', port), CodeHandler).handle_request()

	if authorization_code is None:
		raise OsuAuthenticationException('No authentication code received!')

	# POST the code back to get an access token
	data = {
		'code': authorization_code,
		'client_id': client_id,
		'client_secret': client_secret,
		'redirect_uri': redirect_uri,
		'grant_type': 'authorization_code'
	}
	
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	resp = post(url='https://osu.ppy.sh/oauth/token', data=urlencode(data), headers=headers)

	if resp.status_code == 200:
		return OAuth2AccessToken(resp.json())

	raise OsuAuthenticationException(f'exchange_code_for_token: post request returned status code {resp.status_code}')
