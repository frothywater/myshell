from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myshell.context import Context


class Command(ABC):
    """抽象基类，所有命令类由此继承"""

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

    @abstractmethod
    async def execute(self, args: list[str], context: "Context"):
        """以指定的参数和上下文执行命令"""
        pass

    def help_str(self) -> str:
        """命令的帮助文本字符串"""
        flag_str = "\n".join([f"{key}  {value}" for key, value in self.flags.items()])
        result = f"{self.name}"
        if self.description != "":
            result += f": {self.description}\n"
        if self.usage != "":
            result += f"usage: {self.usage}\n"
        if len(self.flags) > 0:
            result += f"flags: {flag_str}\n"
        return result
