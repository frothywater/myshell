from typing import TYPE_CHECKING, Optional

from myshell.commands import command_dict as original_dict
from myshell.commands.help import HelpCommand
from myshell.commands.other import OtherCommand
from myshell.context import Context

if TYPE_CHECKING:
    from myshell.environment import Environment

from myshell.error import ParsingError

command_dict = original_dict.copy()
command_dict["help"] = HelpCommand

redirect_symbols = ["<", ">", ">>"]


def get_redirect(args: list[str], symbol: str) -> Optional[str]:
    """返回指定重定向符号的路径，若没有则返回`None`，同时将符号和路径从参数列表中删除"""
    result: Optional[str] = None
    while True:
        try:
            index = args.index(symbol)
            if index == len(args) - 1 or args[index + 1] in redirect_symbols:
                raise ParsingError
            result = args[index + 1]
            del args[index : index + 2]
        except ValueError:
            break
    return result


class Instruction:
    """一个指令

    是本程序抽象出来的一个结构，表示一个命令的实例，用以处理单个命令的重定向"""

    def __init__(self, args: list[str], environment: "Environment"):
        self.args = args
        self.name: Optional[str] = None
        if len(self.args) == 0:
            raise ParsingError
        # 在命令字典中找到对应的命令
        if self.args[0] in command_dict:
            self.name = self.args[0]
            del self.args[0]
        self.command_text = " ".join(args)
        self.context = Context(
            environment.in_, environment.out, environment.err, environment
        )  # 从程序环境中得到默认的输入输出流

    def get_output(self) -> tuple[Optional[str], str]:
        """返回(可能的输出文件路径, 文件打开方式)"""
        path = get_redirect(self.args, ">")
        path_appending = get_redirect(self.args, ">>")
        return (path_appending, "a") if path_appending is not None else (path, "w")

    def set_redirect(self):
        """设置命令的重定向"""
        input_path = get_redirect(self.args, "<")
        output_path, write_mode = self.get_output()
        if input_path is not None:
            try:
                self.context.in_ = open(input_path, mode="r", encoding="utf-8")
            except FileNotFoundError:
                print(f"myshell: no such file: {input_path}")
                raise ParsingError
            except OSError:
                print(f"myshell: cannot read file: {input_path}")
                raise ParsingError
        if output_path is not None:
            try:
                self.context.out = open(output_path, mode=write_mode, encoding="utf-8")
            except OSError:
                print(f"myshell: cannot write file: {output_path}")
                raise ParsingError

    async def execute(self):
        """执行指令"""
        command = command_dict[self.name]() if self.name is not None else OtherCommand()
        await command.execute(self.args, self.context)
