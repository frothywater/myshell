from typing import TextIO


class Command:
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

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        pass

    def help_str(self) -> str:
        flag_str = "\n".join([f"{key}  {value}" for key, value in self.flags.items()])
        result = f"{self.name}"
        if self.description != "":
            result += f": {self.description}\n"
        if self.usage != "":
            result += f"usage: {self.usage}\n"
        if len(self.flags) > 0:
            result += f"flags: {flag_str}\n"
        return result
