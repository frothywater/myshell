import os
import signal
import sys
from asyncio.subprocess import Process
from typing import TYPE_CHECKING, Optional, TextIO

if TYPE_CHECKING:
    from myshell.environment import Environment


class Context:
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
        return self.in_.read()

    def write(self, s: str):
        self.out.write(s)

    def error(self, s: str):
        self.err.write(s)

    def close_all(self):
        if self.in_ != sys.stdin and not self.in_suppressed:
            self.in_.close()
        if self.out != sys.stdout:
            self.out.close()
        if self.err != sys.stderr:
            self.err.close()

    @property
    def pid(self) -> int:
        return self.process.pid if self.process is not None else os.getpid()

    def pause(self):
        self.suppress_stdin()
        if self.process is not None:
            self.process.send_signal(signal.SIGTSTP)

    def resume(self):
        self.reset_stdin()
        if self.process is not None:
            self.process.send_signal(signal.SIGCONT)

    def stop(self):
        if self.process is not None:
            self.process.send_signal(signal.SIGINT)

    def suppress_stdin(self):
        if self.in_ == sys.stdin:
            self.in_ = None
            self.in_suppressed = True

    def reset_stdin(self):
        if self.in_suppressed:
            self.in_ = sys.stdin
