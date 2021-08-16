from subprocess import Popen
from typing import Optional, TextIO


class Context:
    def __init__(self, in_: TextIO, out: TextIO, err: TextIO):
        self.in_ = in_
        self.out = out
        self.err = err
        self.process: Optional[Popen] = None
