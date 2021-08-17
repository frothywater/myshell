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
    running = 1
    suspended = 2
    stopped = 3


class Job:
    def __init__(self, s: str, environment: "Environment"):
        args = s.split()
        try:
            ampersand_index = args.index("&")
            if ampersand_index == len(args) - 1:
                self.background: bool = True
                args.pop()
            else:
                raise ParsingError
        except ValueError:
            self.background = False

        self.pipeline = Pipeline(args, environment=environment)
        self.task: Optional[Task] = None
        self.state = JobState.initial

    async def execute(self):
        await self.pipeline.execute()
        self.state = JobState.running

    async def wait(self):
        tasks: list[Task] = []
        for inst in self.pipeline.instructions:
            if inst.context.task is not None:
                tasks.append(inst.context.task)
        if len(tasks) > 0:
            await asyncio.gather(*tasks)
        self.state = JobState.stopped

    def pause(self):
        for inst in self.pipeline.instructions:
            inst.context.pause()
        self.state = JobState.suspended

    def resume(self):
        for inst in self.pipeline.instructions:
            inst.context.resume()
        self.state = JobState.running

    def stop(self):
        for inst in self.pipeline.instructions:
            inst.context.stop()
        self.state = JobState.stopped

    def suppress_stdin(self):
        for inst in self.pipeline.instructions:
            inst.context.suppress_stdin()
        self.background = True

    def reset_stdin(self):
        for inst in self.pipeline.instructions:
            inst.context.reset_stdin()
        self.background = False

    def info(self, index: int):
        result = f"[{index}] {self.state.name}\n"
        for inst in self.pipeline.instructions:
            result += f" - {inst.context.pid} | {inst.command_text}\n"
        return result
