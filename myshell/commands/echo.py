from myshell.command import Command
from myshell.context import Context


class EchoCommand(Command):
    def __init__(self):
        super().__init__("echo", description="print text", usage="echo <text>")

    async def execute(self, args: list[str], context: Context):
        if len(args) > 0:
            context.write(args[0] + "\n")
        context.close_all()
