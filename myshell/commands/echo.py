from myshell.context import Context

from myshell.command import Command


class EchoCommand(Command):
    def __init__(self):
        super().__init__("echo", description="print text", usage="echo <text>")

    def execute(self, args: list[str], context: Context):
        if len(args) > 0:
            context.out.write(args[0] + "\n")
