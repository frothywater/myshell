from copy import copy
from typing import Optional

from myshell.commands import command_dict as original_dict
from myshell.commands.help import HelpCommand
from myshell.commands.other import OtherCommand
from myshell.context import Context
from myshell.error import ParsingError

command_dict = original_dict.copy()
command_dict["help"] = HelpCommand


def get_redirection(args: list[str], symbol: str) -> Optional[str]:
    result: Optional[str] = None
    while True:
        try:
            index = args.index(symbol)
            if index == len(args) - 1 or args[index + 1] in ["<", ">"]:
                raise ParsingError
            result = args[index + 1]
            del args[index : index + 2]
        except ValueError:
            break
    return result


class Instruction:
    def __init__(self, args: list[str], context: Context):
        self.name: Optional[str] = None
        self.context = copy(context)

        input_path = get_redirection(args, "<")
        output_path = get_redirection(args, ">")
        if input_path is not None:
            try:
                self.in_ = open(input_path, mode="r", encoding="utf-8")
            except FileNotFoundError:
                print(f"myshell: no such file: {input_path}")
                raise ParsingError
            except OSError:
                print(f"myshell: cannot read file: {input_path}")
                raise ParsingError
        if output_path is not None:
            try:
                self.out_ = open(output_path, mode="w", encoding="utf-8")
            except OSError:
                print(f"myshell: cannot write file: {output_path}")
                raise ParsingError

        if len(args) == 0:
            raise ParsingError
        if args[0] in command_dict:
            self.name = args[0]
            del args[0]
        self.args = args

    async def execute(self, context: Context):
        command = command_dict[self.name]() if self.name is not None else OtherCommand()
        await command.execute(self.args, self.context)
