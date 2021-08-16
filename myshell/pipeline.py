import os

from myshell.context import Context
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


class Pipeline:
    def __init__(self, s: str, context: Context):
        self.context = context
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
                self.instructions.append(Instruction(part, context=self.context))

    async def execute(self):
        if len(self.instructions) == 0:
            return
        elif len(self.instructions) == 1:
            await self.instructions[0].execute(self.context)
            if self.instructions[0].context.task is not None:
                await self.instructions[0].context.task
        else:
            for index in range(1, len(self.instructions)):
                read, write = os.pipe()
                self.instructions[index - 1].context.out = open(write, mode="w")
                self.instructions[index].context.in_ = open(read, mode="r")
            self.instructions[0].context.in_ = self.context.in_
            self.instructions[len(self.instructions) - 1].context.out = self.context.out
            for instruction in self.instructions:
                await instruction.execute(self.context)
                if instruction.context.task is not None:
                    await instruction.context.task
