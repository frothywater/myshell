import os

from myshell.commands.cd import ChangeDirectoryCommand
from myshell.commands.clr import ClearCommand
from myshell.commands.dir import DirectoryInfoCommand
from myshell.commands.echo import EchoCommand
from myshell.commands.pwd import PrintWorkingDirectoryCommand
from myshell.commands.set import SetEnvironCommand
from myshell.commands.time import TimeCommand
from myshell.commands.umask import UmaskCommand
from myshell.commands.unset import UnsetEnvironCommand

command_dict = {
    "time": TimeCommand,
    "clr": ClearCommand,
    "pwd": PrintWorkingDirectoryCommand,
    "echo": EchoCommand,
    "cd": ChangeDirectoryCommand,
    "set": SetEnvironCommand,
    "unset": UnsetEnvironCommand,
    "umask": UmaskCommand,
    "dir": DirectoryInfoCommand,
}


def execute(args: list[str]):
    if len(args) == 0:
        return
    name = args[0]
    if name in command_dict:
        command = command_dict[name]()
        result = command.execute(args[1:])
        s = result.output.getvalue()
        result.output.close()
        if len(s) > 0:
            if s[-1] == "\n":
                s = s[: len(s) - 1]
            print(s)


def main():
    while True:
        command = input(f"{os.getcwd()} $ ")
        command = command.strip()
        if command == "exit" or command.startswith("exit "):
            break
        execute(command.split())


if __name__ == "__main__":
    main()
