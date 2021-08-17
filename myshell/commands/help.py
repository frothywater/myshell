from myshell.command import Command
from myshell.commands import command_dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help")

    async def execute(self, args: list[str], context: "Context"):
        if len(args) > 0:
            name = args[0]
            if name in command_dict:
                context.write(command_dict[name]().help_str())
            else:
                context.error(f"no entry for {name}\n")
        context.close_all()
