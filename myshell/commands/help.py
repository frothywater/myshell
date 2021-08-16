from io import StringIO
from typing import Optional

from myshell.command import Command
from myshell.dict import command_dict


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help")

    def run(self, args: list[str], input: Optional[StringIO]):
        if len(args) > 0:
            name = args[0]
            if name in command_dict:
                self.log(str(command_dict[name]()))
            else:
                self.error(f"no entry for {name}")
