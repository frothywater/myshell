from myshell.commands.cd import ChangeDirectoryCommand
from myshell.commands.clr import ClearCommand
from myshell.commands.echo import EchoCommand
from myshell.commands.pwd import PrintWorkingDirectoryCommand
from myshell.commands.time import TimeCommand

command_dict = {
    "time": TimeCommand,
    "clr": ClearCommand,
    "pwd": PrintWorkingDirectoryCommand,
    "echo": EchoCommand,
    "cd": ChangeDirectoryCommand,
}


def execute(args: list[str]):
    if len(args) == 0:
        return
    name = args[0]
    if name in command_dict:
        command = command_dict[name]()
        result = command.run(args[1:])
        output = result.output
        if output is not None:
            s = output.getvalue()
            if s[-1] == "\n":
                s = s[: len(s) - 1]
            print(s)
            output.close()


def main():
    while True:
        command = input("$ ")
        command = command.strip()
        if command == "exit" or command.startswith("exit "):
            break
        execute(command.split())


if __name__ == "__main__":
    main()
