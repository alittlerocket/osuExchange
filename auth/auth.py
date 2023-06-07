from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import post
from sys import exit
from urllib.parse import urlencode, urlparse, parse_qs
import webbrowser
import json                    

class OsuAuthenticationException(BaseException):
    def __init__(self, message: str):
        super().__init__(message)

# Allows for customization of GET and POST handling.
class ReqHandler(BaseHTTPRequestHandler):
    path = ''

    # Handling the options request, see why in the README
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # Handles the get request. This includes retriving the authorization code while making
    # a post request to exchange that code for the access token.
    def do_GET(self):
        ReqHandler.path = self.path

        if not self.path.startswith('/?code='):
            return

        # Just using some fancy parsing tools to get the authorization code.
        query_params = parse_qs(urlparse(self.path).query)
        authorization_code = query_params.get('code', [''])[0]

        if ("access_denied" in authorization_code):
            # If the user actually decides to decline authorization, 401 error occurs
            self.send_error(401, "Unauthorized Request")
        else:
            # If successful, we will redirect the user to an Authorization Successful page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authorization Successful!')

        # Shut down the server.
        # server.shutdown()
        # print('here')

class OsuAuthenticator:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, token_endpoint: str, auth_endpoint: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_endpoint = token_endpoint
        self.auth_endpoint = auth_endpoint


    def exchange_authorization_code(self, authorization_code: str) -> dict:
        # Create the payload for the token request
        data = {
            'code': authorization_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        # Headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Send token request
        response = post(url="https://osu.ppy.sh/oauth/token",
                            data=data,
                            headers=headers)
        
        # Handle the response
        if response.status_code == 200: # If successful
            return response.json()

        else: # If failed
            raise OsuAuthenticationException(f"Token request failed with status code {response.status_code}")

    def request_auth(self, client_id):
        params = {
            'client_id' : client_id,            # client_id
            'redirect_uri' : self.redirect_uri,      # redirect_uri
            'response_type' : 'code',           # Also should always be this
            'scope' : 'public identify',        # Should always be this
            'state' : 'randomval'               # For security purposes
        }

        # Format the correct authentication URL
        url = '{}{}{}'.format('https://osu.ppy.sh/oauth/authorize','?',urlencode(params))

        # Open this URL
        webbrowser.open(url)
    
    # Client interface
    # Pass client id as a string
    def get_access_token(self, authorization_code: str) -> dict:
        return self.exchange_authorization_code(authorization_code)

    def refresh_access_token(self, refresh_token: str) -> dict:
        # Necessary body parameters
        data = {
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        # Necessary headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Make the post request.
        response = post('https://osu.ppy.sh/oauth/authorize', 
                        data=data, 
                        headers=headers)

        # If succeeded
        if response.status_code == 200:
            return response.json()

        else: # If failed.
            raise OsuAuthenticationException(f"Token refresh failed with status code {response.status_code}")

def run_server(server_address):
    """Starts the server and listens for requests."""
    print(f"Server up with {server_address[0]}:{server_address[1]}")
    httpd = HTTPServer(server_address, ReqHandler)
    httpd.handle_request()

def parse_uri(redirect_uri: str):
    parse_uri = redirect_uri.split(':')
    return (parse_uri[1][2:], int(parse_uri[-1]))

def get_access_token(client_id: str, client_secret: str, redirect_uri: str):
    authenticator = OsuAuthenticator(client_id, 
                                     client_secret, 
                                     redirect_uri, 
                                     'https://osu.ppy.sh/oauth/authorize', 
                                     'https://osu.ppy.sh/oauth/authorize')

    authenticator.request_auth(client_id)
    run_server(parse_uri(redirect_uri))
    authorization_code = parse_qs(urlparse(ReqHandler.path).query).get('code', [''])[0]
    return authenticator.get_access_token(authorization_code)

