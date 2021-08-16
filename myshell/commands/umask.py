import os

from myshell.context import Context

from myshell.command import Command


class UmaskCommand(Command):
    def __init__(self):
        super().__init__("umask", description="get or set umask", usage="umask [mask]")

    def execute(self, args: list[str], context: Context):
        if len(args) == 0:
            prev_mask = os.umask(0)
            os.umask(prev_mask)
            context.out.write(f"{prev_mask:03o}\n")
        else:
            try:
                mask = int(args[0], 8)
                os.umask(mask)
            except ValueError:
                context.err.write(f"bad symbolic mode operator: {args[0]}\n")
