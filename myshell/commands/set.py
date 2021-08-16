import os

from myshell.command import Command
from myshell.context import Context


class SetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "set", description="show all environment variables", usage="set"
        )

    async def execute(self, args: list[str], context: Context):
        for key, value in os.environ.items():
            context.write(f"{key}={value}\n")
        context.close_all()
