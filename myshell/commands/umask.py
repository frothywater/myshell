import os

from myshell.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class UmaskCommand(Command):
    def __init__(self):
        super().__init__("umask", description="get or set umask", usage="umask [mask]")

    async def execute(self, args: list[str], context: "Context"):
        if len(args) == 0:
            prev_mask = os.umask(0)
            os.umask(prev_mask)
            context.write(f"{prev_mask:03o}\n")
        else:
            try:
                mask = int(args[0], 8)
                os.umask(mask)
            except ValueError:
                context.error(f"bad symbolic mode operator: {args[0]}\n")
        context.close_all()
