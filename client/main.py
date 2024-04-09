#!/usr/bin/env python
"""
program_name is a simple command line tool for interacting with the user and the program_name API.
Date: 2024/04/09
"""


import os
import sys
if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import __version__
from config import Config
import click
import platform
from shell import Shell



# use pyreadline3 instead of readline on windows
is_windows = platform.system() == "Windows"
if is_windows:
    import pyreadline3  as readline # noqa: F401
else:
    import readline


# Setting tab completion parameters
readline.parse_and_bind('tab: complete')

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.command()
@click.version_option(__version__)
@pass_config
def cli(config):
    if config.progConfig.get("showDisclaimer",True):
        print(config.disclaimer)
    """Use the cmd module to create an interactive shell where the user can all the commands such as query, edit, config, show. We will call a class which we will write later as a child of cmd.cmd"""
    

    shell = Shell(config)
    shell.cmdloop()

if __name__ == '__main__':
    cli()
