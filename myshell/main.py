import os

from myshell.commands.help import HelpCommand
from myshell.commands.other import OtherCommand
from myshell.dict import command_dict as original_dict

command_dict = original_dict.copy()
command_dict["help"] = HelpCommand


def execute(args: list[str]):
    if len(args) == 0:
        return
    name = args[0]
    if name in command_dict:
        command = command_dict[name]()
        result = command.execute(args[1:])
    else:
        result = OtherCommand().execute(args)
    result.print()


def set_env():
    print(__file__)
    os.environ["shell"] = __file__


def main():
    set_env()
    while True:
        command = input(f"({os.getcwd()}) $ ")
        command = command.strip()
        if command == "exit" or command.startswith("exit "):
            break
        execute(command.split())


if __name__ == "__main__":
    main()
