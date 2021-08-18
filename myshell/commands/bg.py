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
        manager = context.environment.job_manager
        for arg in args:
            if not (arg.startswith("%") and arg[1:].isnumeric()):
                context.error(f"job not found: {arg}\n")
                continue
            id = int(arg[1:])
            if not manager.is_job_available(id):
                context.error(f"no such job: {arg}\n")
                continue
            if not manager.is_job_suspended(id):
                context.error(f"job is not suspended: {arg}\n")
                continue
            manager.resume_background(id)
        context.close_all()
