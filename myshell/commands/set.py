import os

from myshell.context import Context


from myshell.command import Command


class SetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "set", description="show all environment variables", usage="set"
        )

    def execute(self, args: list[str], context: Context):
        for key, value in os.environ.items():
            context.out.write(f"{key}={value}\n")
