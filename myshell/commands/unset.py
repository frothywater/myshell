import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class UnsetEnvironCommand(Command):
    def __init__(self):
        super().__init__("unset")

    def run(self, args: list[str], input: Optional[StringIO]):
        for key in args:
            if key in os.environ.keys():
                _ = os.environ.pop(key)
