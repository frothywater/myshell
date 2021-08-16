import os
from typing import TextIO

from myshell.command import Command


class UmaskCommand(Command):
    def __init__(self):
        super().__init__("umask", description="get or set umask", usage="umask [mask]")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        if len(args) == 0:
            prev_mask = os.umask(0)
            os.umask(prev_mask)
            out.write(f"{prev_mask:03o}\n")
        else:
            try:
                mask = int(args[0], 8)
                os.umask(mask)
            except ValueError:
                err.write(f"bad symbolic mode operator: {args[0]}\n")
