import asyncio
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.job import Job, JobState


class JobManager:
    def __init__(self, environment: "Environment"):
        self.foreground_job: Optional[Job] = None
        self.background_jobs: list[Optional[Job]] = []
        self.environment = environment

    async def execute(self, s: str):
        job = Job(s, environment=self.environment)
        if job.background:
            job.suppress_stdin()
            index: Optional[int] = self.add_background_job(job)
            self.environment.write(job.info(index))  # type: ignore
        else:
            self.foreground_job = job
            index = None
        await job.execute()
        self.insert_wait_task(index)

    def insert_wait_task(self, index: Optional[int] = None):
        if index is not None and self.background_jobs[index] is not None:
            self.background_jobs[index].task = asyncio.create_task(self.wait_at_background(index))  # type: ignore
        elif self.foreground_job is not None:
            self.foreground_job.task = asyncio.create_task(self.foreground_job.wait())

    async def wait(self):
        if self.foreground_job is not None:
            await self.foreground_job.task

    async def wait_at_background(self, index: int):
        job = self.background_jobs[index]
        if job is not None and job.task is not None:
            await job.wait()
            self.environment.write(job.info(index))

    def add_background_job(self, job: Job) -> int:
        index = 0
        while index < len(self.background_jobs):
            if self.background_jobs[index] is None:
                break
            index += 1
        if index == len(self.background_jobs):
            self.background_jobs.append(job)
        else:
            self.background_jobs[index] = job
        return index

    def pause(self):
        if (
            self.foreground_job is not None
            and self.foreground_job.state == JobState.running
        ):
            job = self.foreground_job
            job.pause()
            job.task.cancel()
            job.task = None
            job.suppress_stdin()
            self.foreground_job = None
            index = self.add_background_job(job)
            self.environment.write(job.info(index))

    def resume(self, index: int, at_background: bool = False):
        if not (
            index < len(self.background_jobs)
            and self.background_jobs[index] is not None
        ):
            self.environment.error(f"bg: no such job %{index}\n")
            return
        if self.background_jobs[index].state == JobState.running:  # type: ignore
            self.environment.error("bg: job already in background\n")
            return

        job: Job = self.background_jobs[index]  # type: ignore
        if at_background:
            self.insert_wait_task(index)
            job.resume()
            self.environment.write(job.info(index))
        else:
            job.reset_stdin()
            self.foreground_job = job
            self.background_jobs[index] = None
            self.insert_wait_task()
            job.resume()

    def stop(self):
        if (
            self.foreground_job is not None
            and self.foreground_job.state == JobState.running
        ):
            job = self.foreground_job
            job.stop()
            job.task.cancel()
            self.foreground_job = None
