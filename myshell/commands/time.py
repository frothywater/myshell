from datetime import datetime

from myshell.command import Command
from myshell.context import Context


class TimeCommand(Command):
    def __init__(self):
        super().__init__(
            "time", description="print current date and time", usage="time"
        )

    async def execute(self, args: list[str], context: Context):
        context.write(datetime.now().strftime("%c") + "\n")
        context.close_all()
