import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.environment import Environment

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
    def __init__(self, args: list[str], environment: "Environment"):
        self.environment = environment
        parts = split(args, "|")
        self.instructions: list[Instruction] = []
        for part in parts:
            if len(part) > 0:
                inst = Instruction(part, environment=self.environment)
                self.instructions.append(inst)

        self.set_pipes()

        for inst in self.instructions:
            if inst.name != "exec":
                inst.set_redirect()

    def set_pipes(self):
        insts = self.instructions
        if len(insts) >= 2:
            for index in range(1, len(insts)):
                read, write = os.pipe()
                insts[index - 1].context.out = open(write, mode="w")
                insts[index].context.in_ = open(read, mode="r")

    async def execute(self):
        for inst in self.instructions:
            await inst.execute()
