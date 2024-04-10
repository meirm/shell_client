import shlex
from client.tools import eprint, strToValue
import requests
from rich import print
import json

def do_ping(shell, args):
    """Pings the server and prints the response."""
    args = shlex.split(args)
    clean = True
    show_headers = False
    if "verbose" in args:
        show_headers = True
        args.remove("verbose")
    if len(args) == 0:
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