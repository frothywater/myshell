from datetime import datetime

from myshell.context import Context

from myshell.command import Command


class TimeCommand(Command):
    def __init__(self):
        super().__init__(
            "time", description="print current date and time", usage="time"
        )

    def execute(self, args: list[str], context: Context):
        context.out.write(datetime.now().strftime("%c") + "\n")
