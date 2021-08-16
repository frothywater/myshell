from abc import ABC, abstractmethod
from io import StringIO
from typing import Optional


class CommandResult:
    def __init__(self, output: StringIO, exit_code: int = 0):
        self.output = output
        self.exit_code = exit_code


class Command(ABC):
    def __init__(
        self,
        name: str,
        description: str = "",
        usage: str = "",
        flags: dict[str, str] = {},
    ):
        self.name = name
        self.description = description
        self.usage = usage
        self.flags = flags
        self.output = StringIO()

    def log(self, s: str):
        self.output.write(s)

    def error(self, s: str):
        print(f"{self.name}: {s}")

    @abstractmethod
    def run(self, args: list[str], input: Optional[StringIO]):
        raise NotImplementedError

    def execute(
        self, args: list[str], input: Optional[StringIO] = None
    ) -> CommandResult:
        self.run(args, input)
        return CommandResult(self.output)

    def __str__(self) -> str:
        flag_str = "\n".join([f"{key}  {value}" for key, value in self.flags.items()])
        result = f"{self.name}"
        if self.description != "":
            result += f": {self.description}\n"
        if self.usage != "":
            result += f"usage: {self.usage}\n"
        if len(self.flags) > 0:
            result += f"flags: {flag_str}"
        return result
