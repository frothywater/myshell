import sys

from myshell.manager import JobManager


class Environment:
    def __init__(self):
        self.in_ = sys.stdin
        self.out = sys.stdout
        self.err = sys.stderr
        self.job_manager = JobManager(self)

    def write(self, s: str):
        self.out.write(s)

    def error(self, s: str):
        self.err.write(s)
