from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class ForegroundCommand(Command):
    def __init__(self):
        super().__init__(
            "fg", description="run suspended job in foreground", usage="fg %<id>"
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
            if manager.is_job_suspended(id):
                manager.resume_foreground(id)
            elif manager.is_job_background(id):
                manager.move_foreground(id)
            else:
                context.error(f"job is not suspended or in background: {arg}\n")
        context.close_all()
