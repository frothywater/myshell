#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.instruction import Instruction


def split(args: list[str], separator: str) -> list[list[str]]:
    """返回按分隔符分割的字符串列表"""
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
    """一组可能包含管道的指令集合

    是本程序抽象出来的一个结构，用以处理命令管道
    """

    def __init__(self, args: list[str], environment: "Environment"):
        self.environment = environment
        parts = split(args, "|")
        self.instructions: list[Instruction] = []
        for part in parts:
            if len(part) > 0:
                inst = Instruction(part, environment=self.environment)
                self.instructions.append(inst)

        # 1. 先处理命令之间的管道
        self.set_pipes()

        # 2. 再处理各个命令的重定向
        for inst in self.instructions:
            if inst.name != "exec":  # 若是`exec`命令则交给其自身解释重定向
                inst.set_redirect()

    def set_pipes(self):
        """设置命令之间的管道"""
        insts = self.instructions
        if len(insts) >= 2:
            for index in range(1, len(insts)):
                read, write = os.pipe()
                insts[index - 1].context.out = open(write, mode="w")
                insts[index].context.in_ = open(read, mode="r")

    async def execute(self):
        """执行这组命令"""
        for inst in self.instructions:
            await inst.execute()
