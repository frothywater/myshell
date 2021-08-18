import asyncio
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.job import Job, JobState


class JobManager:
    def __init__(self, environment: "Environment"):
        self.foreground_job: Optional[Job] = None
        self.background_jobs: list[Optional[Job]] = [None]
        self.environment = environment

    async def execute(self, s: str):
        self.clean_jobs()
        job = Job(s, environment=self.environment)
        if job.initially_background:
            id = self.make_background_place()
            self.background_jobs[id] = job
            await job.execute(id)
        else:
            self.foreground_job = job
            await job.execute()

    async def wait(self):
        try:
            if self.foreground_job is not None:
                await self.foreground_job.task
        except asyncio.CancelledError:
            pass

    def pause(self):
        if self.foreground_job is None:
            return
        id = self.make_background_place()
        self.background_jobs[id] = self.foreground_job
        self.foreground_job = None
        self.background_jobs[id].pause(id)

    def resume_foreground(self, id: int):
        assert self.is_job_suspended(id)
        self.foreground_job = self.background_jobs[id]
        self.background_jobs[id] = None
        self.foreground_job.resume_foreground()  # type: ignore

    def resume_background(self, id: int):
        assert self.is_job_suspended(id)
        self.background_jobs[id].resume_background()  # type: ignore

    def move_foreground(self, id: int):
        assert self.is_job_background(id)
        self.foreground_job = self.background_jobs[id]
        self.background_jobs[id] = None
        self.foreground_job.move_foreground()  # type: ignore

    def stop(self):
        if self.foreground_job is None:
            return
        self.foreground_job.stop()
        self.foreground_job = None

    def is_job_available(self, id: int) -> bool:
        return id < len(self.background_jobs) and self.background_jobs[id] is not None

    def is_job_suspended(self, id: int) -> bool:
        return (
            self.is_job_available(id)
            and self.background_jobs[id].state == JobState.suspended  # type: ignore
        )

    def is_job_background(self, id: int) -> bool:
        return (
            self.is_job_available(id)
            and self.background_jobs[id].state == JobState.background  # type: ignore
        )

    def make_background_place(self) -> int:
        id = 1
        while id < len(self.background_jobs):
            if self.background_jobs[id] is None:
                break
            id += 1
        if id == len(self.background_jobs):
            self.background_jobs.append(None)
        return id

    def clean_jobs(self):
        for index, job in enumerate(self.background_jobs):
            if job is not None and job.state == JobState.stopped:
                self.background_jobs[index] = None
