import os
import sys
import asyncio
from subprocess import Popen


def start_monitor(*args):
    cwd = os.path.abspath(__file__)
    cwd = cwd.rsplit(':', 1)
    scriptpath, scriptname = cwd[-1].rsplit('/', 1)
    sys.path.append(os.path.join(scriptpath, "monitor"))

    # from main import main_async
    # asyncio.run(main_async())

    Popen(['python3', os.path.join(scriptpath, 'monitor/main.py')])
