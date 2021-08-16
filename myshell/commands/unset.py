import os

from myshell.context import Context


from myshell.command import Command


class UnsetEnvironCommand(Command):
    def __init__(self):
        super().__init__(
            "unset",
            description="unset environment variable",
            usage="unset <key> [...keys]",
        )

    def execute(self, args: list[str], context: Context):
        for key in args:
            if key in os.environ.keys():
                _ = os.environ.pop(key)
