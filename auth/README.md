"# auth.py"

This code handles the entirety of the OAuth2 Authorization flow for the
osu! API

"Modules and what they are used for":
- http.server.HTTPServer and http.server.BaseHTTPRequestHandler are used to create the local server.
- requests.post is used to send HTTP POST requests.
- sys.exit is used to terminate the script.
- urllib.parse.urlencode, urllib.parse.urlparse, and urllib.parse.parse_qs are used for URL parsing.
- webbrowser is used to open a web browser for the authorization process.
json is used to handle JSON data.

client ID and client secret:

    What is it?

        A client_secret is a confidential value used in OAuth2 authentication 
        to identify and authenticate a client application. You use it in 
        combination with a client_id to verify the identity and permissions of 
        the client application when interacting with an OAuth2 server.

        Think about it like an additional layer of security to the authentication process.

    For the code, I provided my own client_id and client_secret, and I don't really 
    care if you guys know about it. However, if you would like to learn how to obtain these. 
    You can follow the steps that I wrote in this Google Doc link:

    https://docs.google.com/document/d/1CUrgGzI91LYKZN6Jb-3kgoLBQjLiXTsLNU2KEajiTYc/edit?usp=sharing


Server Details:

    We are going to be running the server on our local machine. In order to tell the 
    computer that, we indicate 'HOST' as 'localhost'. The exact 'PORT' number that 
    the server will use to listen for any incoming requests is arbitrary, but 
    because I'm funny, we're using '6969'

Defining redirect_uri:

    We are going to set the redirect_uri to http://localhost:6969

    This is a URI that the OAuth2 provider, the page that basically wants you to 
    authenticate or whatever, gives that will redirect the user after they 
    click authorize (or cancel).

    If you try to redirect the user without specifying the 'Application Callback 
    URLs' on the osu! website, it will not work. Also, the serve must be 
    running, obviously.

Specifying the token and Auth endpoints:

    The auth_endpoint is set to https://osu.ppy.sh/oauth/authorize. It is the base 
    URL where the user will be redirected for the authorization process (there 
    are some query parameters attached to the end of the link, but this is the base).

    After filling out the necessary parameters, we can make a get request with 
    this information. If the user accepts the authorization, then we will be 
    given an authorization code which can then be traded in for an access token 
    in the following steps.

    The token_endpoint is set to https://osu.ppy.sh/oauth/token. It is the base URL 
    where the server will send a request to exchange the authorization code for 
    an access token.

    What do we use the access token for?

        An access token is a credential that is used to authenticate and authorize 
        requests made by a client application to access protected resources on a 
        server. It is a security token that grants access permissions for a specific 
        user or client application. 
        
        Because we have it, we have permission to access protected resources 
        on behalf of the user.

Making ReqHandler and inheriting it from BaseHTTPRequestHandler:

    Inheriting from BaseHTTPRequestHandler allows us to access functions like do_GET 
    and do_POST so we have customization of how we handle the "GET" and "POST" requests. 
    
    In our case, we're using GET requests to retrieve data from a server and POST to 
    submit our authorization code to process our access token.

    do_OPTIONS is mainly there so we don't do a second GET request, because Google 
    probably is making GET requests in the background when it's caching stuff and tracking you.

    do_GET is overridden to basically do all the heavy lifting. It gets the authorization 
    code, trades it in with the help of "exchange_authorization_code", which sends the 
    correct POST request with all the required parameters, and gets the access token.

        If you would like to learn more about the kinds of parameters they need, I 
        highly suggest reviewing the osu!web documentation on the exchanging of the 
        authorization code for an access token.
    
    Access tokens have expirations. In our case, 84600 seconds is about 23.5 hours. 
    So we can use the refresh_access_token method to refresh our access code without 
    the need of going through the whole authentication process again if we ever need it.

run_server:

    run_server function will create an HTTPServer object as specified by global variables 
    HOST and PORT with ReqHandler as the request handler. We can use serve_forever to 
    start it up and continue until we Ctrl+C out of it.