import os
from typing import TYPE_CHECKING

from myshell.command import Command

if TYPE_CHECKING:
    from myshell.context import Context


class ExecCommand(Command):
    def __init__(self):
        super().__init__(
            "exec",
            description="replace current process, or change stdin/stdout",
            usage="""exec <program>
            exec > file
            exec < file""",
        )

    async def execute(self, args: list[str], context: "Context"):
        if len(args) == 2 and args[0] in ["<", ">"]:
            path = args[1]
            if args[0] == "<":
                try:
                    context.environment.in_ = open(path, mode="r", encoding="utf-8")
                except FileNotFoundError:
                    context.error(f"no such file: {path}\n")
                except OSError:
                    context.error(f"cannot read file: {path}]\n")
                finally:
                    context.close_all()
            elif args[0] == ">":
                try:
                    context.environment.out = open(path, mode="w", encoding="utf-8")
                except OSError:
                    context.error(f"cannot write file: {path}\n")
                finally:
                    context.close_all()
        else:
            try:
                os.execvp(args[0], args)
            except ValueError:
                context.error("need a program\n")
            except OSError:
                context.error(f"cannot run program: {' '.join(args)}\n")
            finally:
                context.close_all()
