import shlex
from client.tools import eprint, strToValue
import requests
from rich import print

def do_login(shell, args):
    """Login to the server. Usage: login <uri> <username> <password>"""
    args = shlex.split(args)
    clean = True
    show_headers = False
    if "verbose" in args:
        show_headers = True
        args.remove("verbose")
    if len(args) == 3:
        drf_url = shell._config.progConfig["drf_host"] + "/token/"
        # get the CSRF token
        session = requests.Session()
        # POST the login data
        data = {
            "username": args[1],
            "password": args[2]
        }
        response = session.post(drf_url, json=data)
        if show_headers:
            eprint(f"HEADERS: {response.headers}")
        # see if we are logged in
        if response.status_code == 200:
            eprint("Logged in.")
            # Get the token from /token/
            jwt_token = response.json().get('access')
            if jwt_token:
                # Save the JWT in your configuration for later use
                shell._config.progConfig["jwt_token"] = jwt_token
                shell._config.progConfig["session"] = session
            else:
                eprint("JWT token not found in login response.")
                return
        else:
            eprint("Login failed.")
            print(response.status_code)
        return
    else:
        eprint("Usage: login <uri> <username> <password> [verbose]")
    if not clean:
        pass