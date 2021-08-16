import os

from myshell.job import Job


def set_env():
    os.environ["shell"] = __file__


def main():
    set_env()
    while True:
        s = input(f"({os.getcwd()}) $ ")
        s = s.strip()
        if s == "exit" or s.startswith("exit "):
            break
        job = Job(s)
        job.execute()


if __name__ == "__main__":
    main()
