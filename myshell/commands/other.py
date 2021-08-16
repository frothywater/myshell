import os
import subprocess
from typing import TextIO

from myshell.command import Command


class OtherCommand(Command):
    def __init__(self):
        super().__init__("myshell")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        env = os.environ.copy()
        env["parent"] = os.getcwd()
        try:
            subprocess.run(args, stdin=in_, stdout=out, stderr=err, env=env)
        except FileNotFoundError:
            err.write(f"no such file or directory: {args[0]}")
        except subprocess.SubprocessError:
            err.write("error")
