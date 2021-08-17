import os

from myshell.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class ClearCommand(Command):
    def __init__(self):
        super().__init__("clr", description="clear console screen", usage="clr")

    async def execute(self, args: list[str], context: "Context"):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")
        context.close_all()
