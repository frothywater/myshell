import asyncio
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.job import Job, JobState


class JobManager:
    """事务管理器，用以调度前台和后台事务"""

    def __init__(self, environment: "Environment"):
        self.foreground_job: Optional[Job] = None
        self.background_jobs: list[Optional[Job]] = [None]
        self.environment = environment

    async def execute(self, s: str):
        """执行一行命令，按指定分配到前台或后台"""
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
        """等待前台事务完成，并屏蔽`CancelError`"""
        try:
            if self.foreground_job is not None:
                await self.foreground_job.task
        except asyncio.CancelledError:
            pass

    def pause(self):
        """暂停前台事务并分配到后台"""
        if self.foreground_job is None:
            return
        id = self.make_background_place()
        self.background_jobs[id] = self.foreground_job
        self.foreground_job = None
        self.background_jobs[id].pause(id)

    def resume_foreground(self, id: int):
        """将后台已暂停的事务恢复到前台"""
        assert self.is_job_suspended(id)
        self.foreground_job = self.background_jobs[id]
        self.background_jobs[id] = None
        self.foreground_job.resume_foreground()  # type: ignore

    def resume_background(self, id: int):
        """恢复后台已暂停的事务"""
        assert self.is_job_suspended(id)
        self.background_jobs[id].resume_background()  # type: ignore

    def move_foreground(self, id: int):
        """将后台正在运行的事务移动到前台"""
        assert self.is_job_background(id)
        self.foreground_job = self.background_jobs[id]
        self.background_jobs[id] = None
        self.foreground_job.move_foreground()  # type: ignore

    def stop(self):
        """终止前台事务"""
        if self.foreground_job is None:
            return
        self.foreground_job.stop()
        self.foreground_job = None

    def is_job_available(self, id: int) -> bool:
        """返回是否存在指定编号的事务"""
        return id < len(self.background_jobs) and self.background_jobs[id] is not None

    def is_job_suspended(self, id: int) -> bool:
        """返回指定编号的事务是否已暂停"""
        return (
            self.is_job_available(id)
            and self.background_jobs[id].state == JobState.suspended  # type: ignore
        )

    def is_job_background(self, id: int) -> bool:
        """返回指定编号的事务是否在后台"""
        return (
            self.is_job_available(id)
            and self.background_jobs[id].state == JobState.background  # type: ignore
        )

    def make_background_place(self) -> int:
        """返回后台事务列表中一个空余位置的编号，若不存在则创建一个"""
        id = 1
        while id < len(self.background_jobs):
            if self.background_jobs[id] is None:
                break
            id += 1
        if id == len(self.background_jobs):
            self.background_jobs.append(None)
        return id

    def clean_jobs(self):
        """删除后台事务列表中已终止的事务"""
        for index, job in enumerate(self.background_jobs):
            if job is not None and job.state == JobState.stopped:
                self.background_jobs[index] = None
