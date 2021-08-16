import os
import signal
import sys

from myshell.job import Job


class App:
    def __init__(self):
        self.in_ = sys.stdin
        self.out = sys.stdout
        self.err = sys.stderr

    def handle_sigint(self, signum, frame):
        pass

    def handle_sigtstp(self, signum, frame):
        pass

    def bootstrap(self):
        os.environ["shell"] = __file__
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTSTP, self.handle_sigtstp)

    def run(self):
        while True:
            s = input(f"({os.getcwd()}) $ ")
            s = s.strip()
            if s == "exit" or s.startswith("exit "):
                break
            job = Job(s)
            job.execute()


app = App()


def main():
    app.bootstrap()
    app.run()


if __name__ == "__main__":
    main()
