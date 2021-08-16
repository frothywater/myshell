import os
import subprocess
from io import StringIO
from typing import Optional

from myshell.command import Command


class OtherCommand(Command):
    def __init__(self):
        super().__init__("other")

    def run(self, args: list[str], input: Optional[StringIO]):
        input_str = input.getvalue() if input is not None else None
        env = os.environ.copy()
        env["parent"] = os.getcwd()
        try:
            result = subprocess.run(
                args, text=True, input=input_str, capture_output=True, env=env
            )
            self.log(result.stdout)
        except FileNotFoundError:
            self.error(f"no such file or directory: {args[0]}")
        except subprocess.SubprocessError:
            self.error("error")
