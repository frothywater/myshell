import asyncio
import os
from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class OtherCommand(Command):
    def __init__(self):
        super().__init__("myshell")

    async def execute(self, args: list[str], context: "Context"):
        env = os.environ.copy()
        env["parent"] = os.getcwd()
        try:
            context.process = await asyncio.create_subprocess_exec(
                *args,
                env=env,
                stdin=context.in_,
                stdout=context.out,
                stderr=context.err,
            )
        except FileNotFoundError:
            context.error(f"no such file or directory: {args[0]}\n")
