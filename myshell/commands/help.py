from typing import TextIO

from myshell.command import Command
from myshell.commands import command_dict


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        if len(args) > 0:
            name = args[0]
            if name in command_dict:
                out.write(command_dict[name]().help_str())
            else:
                err.write(f"no entry for {name}\n")
