import os
from io import StringIO
from typing import Callable, Optional

from myshell.command import Command


class TestCommand(Command):
    file_check_dict: dict[str, Callable[[str], bool]] = {
        "-d": lambda path: os.path.isdir(path),
        "-f": lambda path: os.path.isfile(path),
        "-L": lambda path: os.path.islink(path),
    }

    number_check_dict: dict[str, Callable[[int, int], bool]] = {
        "-eq": lambda a, b: a == b,
        "-ne": lambda a, b: a != b,
        "-gt": lambda a, b: a > b,
        "-ge": lambda a, b: a >= b,
        "-lt": lambda a, b: a < b,
        "-le": lambda a, b: a <= b,
    }

    def __init__(self):
        super().__init__(
            "test",
            description="test expression related to file or numbers",
            usage="""test [-d file] [-f file] [-h file] [-L file]
[num -eq num] [num -ne num] [num -gt num] [num -ge num] [num -lt num] [num -le num]

-f      checks if file is an ordinary file
-d      checks if file is a directory
-L      checks if file is a symbolic link

-eq     checks if the value of two operands are equal or not
-ne     checks if the value of two operands are equal or not
-gt     checks if the value of left operand is greater than the value of right operand
-lt     checks if the value of left operand is less than the value of right operand
-ge     checks if the value of left operand is greater than or equal to the value of right operand
-le     checks if the value of left operand is less than or equal to the value of right operand""",
        )

    def test_file(self, flag: str, path: str) -> bool:
        return self.file_check_dict[flag](path)

    def test_number(self, flag: str, num1: int, num2: int) -> bool:
        return self.number_check_dict[flag](num1, num2)

    def run(self, args: list[str], input: Optional[StringIO]):
        if len(args) == 2 and args[0] in self.file_check_dict:
            result = self.test_file(flag=args[0], path=args[1])
            self.log(f"exit {int(result)}")
        elif len(args) == 3 and args[1] in self.number_check_dict:
            try:
                num1 = int(args[0], 10)
            except ValueError:
                self.error(f"not a number: {args[0]}")
            try:
                num2 = int(args[2], 10)
            except ValueError:
                self.error(f"not a number: {args[2]}")
            result = self.test_number(flag=args[1], num1=num1, num2=num2)
            self.log(f"exit {int(not result)}")
