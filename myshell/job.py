import asyncio
from asyncio import Task
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.error import ParsingError
from myshell.pipeline import Pipeline


class JobState(Enum):
    initial = 0
    foreground = 1
    background = 2
    suspended = 3
    stopped = 4


def check_background(args: list[str]) -> bool:
    try:
        ampersand_index = args.index("&")
        if ampersand_index == len(args) - 1:
            args.pop()
            return True
        else:
            raise ParsingError
    except ValueError:
        return False


class Job:
    def __init__(self, s: str, environment: "Environment"):
        args = s.split()
        self.initially_background = check_background(args)
        self.pipeline = Pipeline(args, environment=environment)
        self.id: Optional[int] = None
        self.state = JobState.initial
        self.environment = environment

    async def execute(self, id: Optional[int] = None):
        if self.initially_background:
            assert id is not None
            self.id = id
            self.state = JobState.background
            self.suppress_stdin()
        else:
            self.state = JobState.foreground
        await self.pipeline.execute()
        self.task: Task = asyncio.create_task(self.wait())

    async def wait(self):
        try:
            coroutines = []
            for inst in self.pipeline.instructions:
                if inst.context.process is not None:
                    coroutines.append(inst.context.process.wait())
            await asyncio.gather(*coroutines)
            if self.state == JobState.background:
                self.state = JobState.stopped
                self.environment.write(self.info)
        except asyncio.CancelledError:
            self.task = None
            raise

    def pause(self, id: int):
        assert self.state == JobState.foreground
        for inst in self.pipeline.instructions:
            inst.context.pause()
        self.id = id
        self.task.cancel()
        self.state = JobState.suspended
        self.environment.write(self.info)

    def resume_foreground(self):
        assert self.state == JobState.suspended
        for inst in self.pipeline.instructions:
            inst.context.resume()
        self.id = None
        self.task = asyncio.create_task(self.wait())
        self.state = JobState.foreground

    def resume_background(self):
        assert self.state == JobState.suspended
        self.suppress_stdin()
        for inst in self.pipeline.instructions:
            inst.context.resume()
        self.task = asyncio.create_task(self.wait())
        self.state = JobState.background
        self.environment.write(self.info)

    def move_foreground(self):
        assert self.state == JobState.background
        self.reset_stdin()
        self.id = None
        self.state = JobState.foreground

    def stop(self):
        assert self.state == JobState.foreground
        for inst in self.pipeline.instructions:
            inst.context.stop()
        self.task.cancel()
        self.state = JobState.stopped

    def suppress_stdin(self):
        for inst in self.pipeline.instructions:
            inst.context.suppress_stdin()

    def reset_stdin(self):
        for inst in self.pipeline.instructions:
            inst.context.reset_stdin()

    @property
    def info(self) -> str:
        result = f"\n[{self.id}] {self.state.name}\n"
        for inst in self.pipeline.instructions:
            result += f" - {inst.context.pid} | {inst.command_text}\n"
        return result
