from myshell.context import Context

from myshell.command import Command
from myshell.commands import command_dict


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help")

    def execute(self, args: list[str], context: Context):
        if len(args) > 0:
            name = args[0]
            if name in command_dict:
                context.out.write(command_dict[name]().help_str())
            else:
                context.err.write(f"no entry for {name}\n")
