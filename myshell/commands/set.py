import os
from typing import TextIO


from myshell.command import Command


class SetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "set", description="show all environment variables", usage="set"
        )

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        for key, value in os.environ.items():
            out.write(f"{key}={value}\n")
