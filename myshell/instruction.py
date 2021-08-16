from typing import Optional, TextIO

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
    def __init__(self, args: list[str]):
        self.name: Optional[str] = None
        self.input_file: Optional[TextIO] = None
        self.output_file: Optional[TextIO] = None

        input_path = get_redirection(args, "<")
        output_path = get_redirection(args, ">")

        if input_path is not None:
            try:
                self.input_file = open(input_path, mode="r", encoding="utf-8")
            except FileNotFoundError:
                print(f"myshell: no such file: {input_path}")
                raise ParsingError
            except OSError:
                print(f"myshell: cannot read file: {input_path}")
                raise ParsingError
        if output_path is not None:
            try:
                self.output_file = open(output_path, mode="w", encoding="utf-8")
            except OSError:
                print(f"myshell: cannot write file: {output_path}")
                if self.input_file is not None:
                    self.input_file.close()
                raise ParsingError

        if len(args) == 0:
            raise ParsingError
        if args[0] in command_dict:
            self.name = args[0]
            del args[0]
        self.args = args

    def execute(self, fallback_in: TextIO, fallback_out: TextIO, err: TextIO):
        command = command_dict[self.name]() if self.name is not None else OtherCommand()
        in_ = self.input_file if self.input_file is not None else fallback_in
        out = self.output_file if self.output_file is not None else fallback_out
        self.context = Context(in_, out, err)
        command.execute(self.args, self.context)
        if self.input_file is not None:
            self.input_file.close()
        if self.output_file is not None:
            self.output_file.close()
