from myshell.commands.cd import ChangeDirectoryCommand
from myshell.commands.clr import ClearCommand
from myshell.commands.dir import DirectoryInfoCommand
from myshell.commands.echo import EchoCommand
from myshell.commands.pwd import PrintWorkingDirectoryCommand
from myshell.commands.set import SetEnvironCommand
from myshell.commands.test import TestCommand
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
    "test": TestCommand,
}
