from myshell.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class ForegroundCommand(Command):
    def __init__(self):
        super().__init__(
            "fg", description="run suspended job in foreground", usage="fg %<id>"
        )

    async def execute(self, args: list[str], context: "Context"):
        for arg in args:
            if not (arg.startswith("%") and arg[1:].isnumeric()):
                context.error(f"job not found: {arg}\n")
                continue
            num = int(arg[1:])
            context.environment.job_manager.resume(num)
        context.close_all()
