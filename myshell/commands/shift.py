import sys
from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class ShiftCommand(Command):
    def __init__(self):
        super().__init__("shift", description="shift arguments", usage="shift <num>")

    async def execute(self, args: list[str], context: "Context"):
        if len(args) > 0 and args[0].isnumeric():
            for i in range(0, int(args[0])):
                if len(sys.argv) > 0:
                    del sys.argv[0]
        context.close_all()
