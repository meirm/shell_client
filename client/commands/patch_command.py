import shlex
from client.tools import eprint, strToValue
import requests
import json
from rich import print

def do_patch(shell, args):
    """Send a PATCH request to the server and prints the response."""
    clean = True
    show_headers = False
    if "verbose" in args:
        show_headers = True
        args = args.replace("verbose", "")
    args = args.strip()
    if len(args) == 0:
        eprint("No URL provided.")
        return
    uri, data = args.split(" ", 1) if " " in args else (args, "")
    url = shell._config.progConfig["drf_host"] + uri
    data = data.strip()
    if data:
        if "session" in shell._config.progConfig:
            if "jwt_token" not in shell._config.progConfig:
                eprint("No JWT token found.")
                return
            jwt_token = shell._config.progConfig["jwt_token"]
            response = shell._config.progConfig["session"].patch(url, data=data, headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/json", "Content-Type": "application/json" })
        else:
            eprint("No session found.")
            return
        if show_headers:
            eprint(f"HEADERS: {response.headers}")
        # print the response
        print(json.dumps(response.json(), indent=4))
        return
    else:
        eprint("No data provided.")
    if not clean:
        pass