import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class UmaskCommand(Command):
    def __init__(self):
        super().__init__("umask")

    def run(self, args: list[str], input: Optional[StringIO]):
        if len(args) == 0:
            prev_mask = os.umask(0)
            os.umask(prev_mask)
            self.log(f"{prev_mask:03o}")
        else:
            try:
                mask = int(args[0], 8)
                os.umask(mask)
            except ValueError:
                self.error(f"bad symbolic mode operator: {args[0]}")
