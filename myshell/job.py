import sys
from io import StringIO

from myshell.error import ParsingError
from myshell.instruction import Instruction


def split(args: list[str], separator: str) -> list[list[str]]:
    current: list[str] = []
    result: list[list[str]] = []
    for arg in args:
        if arg == separator:
            result.append(current)
            current = []
        else:
            current.append(arg)
    if len(current) > 0:
        result.append(current)
    return result


class Job:
    def __init__(self, s: str):
        args = s.split()

        try:
            ampersand_index = args.index("&")
            if ampersand_index == len(args) - 1:
                self.background = True
                args.pop()
            else:
                raise ParsingError
        except ValueError:
            self.background = False

        parts = split(args, "|")
        self.instructions: list[Instruction] = []
        for part in parts:
            if len(part) > 0:
                self.instructions.append(Instruction(part))

    def execute(self):
        if len(self.instructions) == 0:
            return
        elif len(self.instructions) == 1:
            self.instructions[0].execute(sys.stdin, sys.stdout, sys.stderr)
            return

        in_buffer = StringIO()
        out_buffer = StringIO()
        for index, instruction in enumerate(self.instructions):
            in_ = sys.stdin if index == 0 else in_buffer
            out = sys.stdout if index == len(self.instructions) - 1 else out_buffer
            instruction.execute(in_, out, sys.stderr)
            in_buffer.close()
            in_buffer = out_buffer
            in_buffer.seek(0)
            out_buffer = StringIO()
        in_buffer.close()
        out_buffer.close()
