import asyncio
import os
import signal
import sys

from myshell.context import Context
from myshell.pipeline import Pipeline


class App:
    def __init__(self):
        self.context = Context(sys.stdin, sys.stdout, sys.stderr)

    def handle_sigint(self, signum, frame):
        pass

    def handle_sigtstp(self, signum, frame):
        pass

    def bootstrap(self):
        os.environ["shell"] = __file__
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTSTP, self.handle_sigtstp)

    async def run(self):
        while True:
            s = input(f"({os.getcwd()}) $ ")
            s = s.strip()
            if s == "exit" or s.startswith("exit "):
                break
            pipeline = Pipeline(s, context=self.context)
            await pipeline.execute()


def main():
    app = App()
    app.bootstrap()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
