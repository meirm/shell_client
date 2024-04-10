import shlex
from client.tools import eprint, strToValue
import requests
import json 
from rich import print

def do_get(shell, args):
    """Send a GET request to the server and prints the response."""
    args = shlex.split(args)
    clean = True
    show_headers = False
    if "verbose" in args:
        show_headers = True
        args.remove("verbose")
    if len(args) == 1:
        drf_url = shell._config.progConfig["drf_host"] + args[0]
        # send a GET request to the server as json
        # request json response
        if "session" in shell._config.progConfig:
            if "jwt_token" not in shell._config.progConfig:
                eprint("No JWT token found.")
                return
            jwt_token = shell._config.progConfig["jwt_token"]
            
            response = shell._config.progConfig["session"].get(drf_url, headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/json", "Content-Type": "application/json", })
        else:
            eprint("No session found.")
            return
        if show_headers:
            eprint(f"HEADERS: {response.headers}")
        # print the response
        print(json.dumps(response.json(), indent=4))
        return
    elif len(args) == 0:
        drf_url = shell._config.progConfig["drf_host"] + "/"
        # send a GET request to the server
        response = requests.get(drf_url)
        if show_headers:
            eprint(f"HEADERS: {response.headers}")
        # print the response
        print(json.dumps(response.json(), indent=4))
        return
    else:
        eprint("Unrecognized parameter.")
    if not clean:
        pass