import sys
from asyncio import Task
from asyncio.subprocess import Process
from typing import Optional, TextIO


class Context:
    def __init__(self, in_: TextIO, out: TextIO, err: TextIO):
        self.in_ = in_
        self.out = out
        self.err = err
        self.process: Optional[Process] = None
        self.task: Optional[Task] = None

    def read(self) -> str:
        return self.in_.read()

    def write(self, s: str):
        self.out.write(s)

    def error(self, s: str):
        self.err.write(s)

    def close_all(self):
        if self.in_ != sys.stdin:
            self.in_.close()
        if self.out != sys.stdout:
            self.out.close()
        if self.err != sys.stderr:
            self.err.close()
