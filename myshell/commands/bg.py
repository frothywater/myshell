from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class BackgroundCommand(Command):
    def __init__(self):
        super().__init__(
            "bg", description="run suspended job in background", usage="bg %<id>"
        )

    async def execute(self, args: list[str], context: "Context"):
        for arg in args:
            if not (arg.startswith("%") and arg[1:].isnumeric()):
                context.error(f"job not found: {arg}\n")
                continue
            num = int(arg[1:])
            context.environment.job_manager.resume(num, at_background=True)
        context.close_all()
