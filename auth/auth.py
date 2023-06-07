from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import post
from sys import exit
from urllib.parse import urlencode, urlparse, parse_qs
import webbrowser
import json                    

# The client id and client secret associated
client_id: str
client_secret: str

# We're hosting the server locally and we will be using funny port 
HOST: str = 'localhost'
PORT: int = 6969

# We will be using from now on, so make sure nothing interferes with it
redirect_uri: str = f'http://localhost:{PORT}'    

# We will send a request to the osu! token endpoint and retrieve the access token
# with this base_url. It can also be used to refresh the access token
token_endpoint: str = "https://osu.ppy.sh/oauth/token"

# OAuth2 endpoint
auth_endpoint: str = "https://osu.ppy.sh/oauth/authorize"

class OsuAuthenticationException(BaseException):
    def __init__(self, message: str):
        super().__init__(message)

# Allows for customization of GET and POST handling.
class ReqHandler(BaseHTTPRequestHandler):
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
        if self.path == '/favicon.ico':
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
            self.server.shutdown()
            exchange_authorization_code(authorization_code)


def exchange_authorization_code(authorization_code):
    # Create the payload for the token request
    data = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    # Headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send token request
    response = post(url=token_endpoint,
                        data=data,
                        headers=headers)
    
    # Handle the response
    if response.status_code == 200: # If successful
        token_data = response.json()
        
        # Store the info into a json file
        with open('config.json', 'w') as file:
            file.write(json.dumps(token_data, indent=4))

    else: # If failed
        raise OsuAuthenticationException(f"Token request failed with status code {response.status_code}")

def refresh_access_token(refresh_token):
    # Necessary body parameters
    data = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token'
    }

    # Necessary headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the post request.
    response = post(token_endpoint, data=data, headers=headers)

    # If succeeded
    if response.status_code == 200:
        token_data = response.json()
        
        # Store the info into a json file
        with open('config.json', 'w') as file:
            file.write(json.dumps(token_data, indent=4))
    else: # If failed.
        print(f"Token refresh failed with status code {response.status_code}")
        exit(1)

def request_auth(client_id):
    params = {
        'client_id' : client_id,            # client_id
        'redirect_uri' : redirect_uri,      # redirect_uri
        'response_type' : 'code',           # Also should always be this
        'scope' : 'public identify',        # Should always be this
        'state' : 'randomval'               # For security purposes
    }

    # Format the correct authentication URL
    url = '{}{}{}'.format(auth_endpoint,'?',urlencode(params))

    # Open this URL
    webbrowser.open(url)

def run_server():
    # Create an HTTPServer object with the desired host and port
    server = HTTPServer((HOST, PORT), ReqHandler)

    # Start it
    print("Server up with {}:{}".format(HOST, PORT))
    server.serve_forever()

# Client interface
# Pass client id as a string
def login(_client_id: str, _client_secret: str):
    global client_id, client_secret
    client_id = _client_id
    client_secret = _client_secret

    request_auth(client_id)
    run_server()

# Run the server
if __name__ == "__main__":
    login(client_id, client_secret)
