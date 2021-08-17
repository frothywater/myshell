import os

from myshell.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class UnsetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "unset",
            description="unset environment variable",
            usage="unset <key> [...keys]",
        )

    async def execute(self, args: list[str], context: "Context"):
        for key in args:
            if key in os.environ.keys():
                _ = os.environ.pop(key)
        context.close_all()
