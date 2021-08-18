import asyncio
import os
import signal

import aioconsole

from myshell.environment import Environment
from myshell.error import ParsingError


class App:
    def __init__(self):
        self.environment = Environment()
        self.job_manager = self.environment.job_manager

    def handle_sigint(self, signum, frame):
        self.job_manager.stop()

    def handle_sigtstp(self, signum, frame):
        self.job_manager.pause()

    def bootstrap(self):
        os.environ["shell"] = __file__
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTSTP, self.handle_sigtstp)

    async def run(self):
        while True:
            s = await aioconsole.ainput(f"({os.getcwd()}) $ ")
            s = s.strip()
            if s == "exit" or s.startswith("exit "):
                break
            try:
                await self.job_manager.execute(s)
                await self.job_manager.wait()
            except ParsingError:
                self.environment.error("myshell: parsing error\n")


def main():
    app = App()
    app.bootstrap()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
