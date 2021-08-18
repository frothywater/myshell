from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class JobsCommand(Command):
    def __init__(self):
        super().__init__(
            "jobs", description="print information about background jobs", usage="jobs"
        )

    async def execute(self, args: list[str], context: "Context"):
        for job in context.environment.job_manager.background_jobs:
            if job is not None:
                context.write(job.info)
        context.close_all()
