import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class SetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "set", description="show all environment variables", usage="set"
        )

    def run(self, args: list[str], input: Optional[StringIO]):
        for key, value in os.environ.items():
            self.log(f"{key}={value}\n")
