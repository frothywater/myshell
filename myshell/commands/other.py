import os
from io import UnsupportedOperation
from subprocess import PIPE, Popen, SubprocessError
from typing import IO

from myshell.command import Command
from myshell.context import Context


def is_regular_file(f: IO) -> bool:
    try:
        f.fileno()
    except UnsupportedOperation:
        return False
    return True


class OtherCommand(Command):
    def __init__(self):
        super().__init__("myshell")

    def execute(self, args: list[str], context: Context):
        env = os.environ.copy()
        env["parent"] = os.getcwd()
        in_ = context.in_
        out = context.out
        err = context.err
        try:
            context.process = Popen(
                args=args,
                env=env,
                text=True,
                stdin=in_ if is_regular_file(in_) else PIPE,
                stdout=out if is_regular_file(out) else PIPE,
                stderr=err if is_regular_file(err) else PIPE,
            )
            out_str, err_str = context.process.communicate(
                input=None if is_regular_file(in_) else in_.read()
            )
            if out_str is not None:
                out.write(out_str)
            if err_str is not None:
                err.write(err_str)
        except FileNotFoundError:
            context.err.write(f"no such file or directory: {args[0]}\n")
        except SubprocessError:
            context.err.write("error\n")
