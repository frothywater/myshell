import os
from typing import TextIO


from myshell.command import Command


class UnsetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "unset",
            description="unset environment variable",
            usage="unset <key> [...keys]",
        )

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        for key in args:
            if key in os.environ.keys():
                _ = os.environ.pop(key)
