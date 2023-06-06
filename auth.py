from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import post
from sys import exit
from webbrowser import open
from urllib.parse import urlencode, urlparse, parse_qs                    

# The client id and client secret associated with my account
client_id: int = 22257
client_secret: str = '6u2R8t1zbjA3uLY0Cy8MrjIeF79qFnqPyBqBhHP3'

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
            # and store the access token in a new file.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authorization Successful!')

            access_token = self.exchange_authorization_code(authorization_code)
            print("\n\nHere is the access token: " + access_token)


    def exchange_authorization_code(self, authorization_code):
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
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in')
            return access_token
        else: # If failed
            print(f"Token request failed with status code {response.status_code}")
            exit(1)

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
            new_access_token = token_data.get('access_token')
            new_refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in')
        else: # If failed.
            print(f"Token refresh failed with status code {response.status_code}")

def requestAuth():
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
    open(url)

def run_server():
    # Create an HTTPServer object with the desired host and port
    server = HTTPServer((HOST, PORT), ReqHandler)

    # Start it
    print("Server up with {}:{}".format(HOST, PORT))
    server.serve_forever()

# Run the server
# if __name__ == "__main__":
#     requestAuth()
#     run_server()
    
