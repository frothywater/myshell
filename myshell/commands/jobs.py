from myshell.command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class JobsCommand(Command):
    def __init__(self):
        super().__init__(
            "jobs", description="print information about background jobs", usage="jobs"
        )

    async def execute(self, args: list[str], context: "Context"):
        jobs = context.environment.job_manager.background_jobs
        for index, job in enumerate(jobs):
            if job is not None:
                context.write(job.info(index))
        context.close_all()
