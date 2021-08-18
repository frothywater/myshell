#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import signal
import sys
from asyncio.subprocess import Process
from typing import TYPE_CHECKING, Optional, TextIO

if TYPE_CHECKING:
    from myshell.environment import Environment


class Context:
    """命令执行时的上下文

    是本程序抽象出来的一个结构，将命令与其实际运行时的上下文区分开来，包含了输入输出流和整个程序的环境。
    上下文包含整个程序的环境是为了给诸如`bg`, `fg`, `jobs`这样控制shell本身的命令提供环境。"""

    def __init__(
        self,
        in_: TextIO,
        out: TextIO,
        err: TextIO,
        environment: "Environment",
    ):
        self.in_ = in_
        self.out = out
        self.err = err
        self.environment = environment
        self.process: Optional[Process] = None
        self.in_suppressed: bool = False

    def read(self) -> str:
        """从指定输入流中读入"""
        return self.in_.read()

    def write(self, s: str):
        """向指定输出流中写入"""
        self.out.write(s)

    def error(self, s: str):
        """向指定错误流中写入"""
        self.err.write(s)

    def close_all(self):
        """关闭除了标准流之外的输入、输出、错误流"""
        if self.in_ != sys.stdin and not self.in_suppressed:
            self.in_.close()
        if self.out != sys.stdout:
            self.out.close()
        if self.err != sys.stderr:
            self.err.close()

    @property
    def pid(self) -> int:
        """返回进程id"""
        return self.process.pid if self.process is not None else os.getpid()

    def pause(self):
        """向指定错误流中写入"""
        self.suppress_stdin()
        if self.process is not None:
            self.process.send_signal(signal.SIGTSTP)

    def resume(self):
        """向指定错误流中写入"""
        self.reset_stdin()
        if self.process is not None:
            self.process.send_signal(signal.SIGCONT)

    def stop(self):
        """向指定错误流中写入"""
        if self.process is not None:
            self.process.send_signal(signal.SIGINT)

    def suppress_stdin(self):
        """阻止命令从标准输入中读入"""
        if self.in_ == sys.stdin:
            self.in_ = None
            self.in_suppressed = True

    def reset_stdin(self):
        """恢复命令从标准输入中读入"""
        if self.in_suppressed:
            self.in_ = sys.stdin
