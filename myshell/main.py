#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import os
import signal
import sys
from typing import Optional, TextIO

import aioconsole

from myshell.environment import Environment
from myshell.error import ParsingError


class App:
    """顶层类，程序起始点"""

    def __init__(self):
        self.environment = Environment()  # 程序环境
        self.job_manager = self.environment.job_manager
        self.file: Optional[TextIO] = None

    def handle_sigint(self, signum, frame):
        """停止信号的回调函数"""
        self.job_manager.stop()

    def handle_sigtstp(self, signum, frame):
        """暂停信号的回调函数"""
        self.job_manager.pause()

    def bootstrap(self):
        """初始化，处理文件输入"""
        if len(sys.argv) > 1:
            path = sys.argv[1]
            try:
                self.file = open(path, mode="r", encoding="utf-8")
            except FileNotFoundError:
                self.environment.error(f"myshell: file not found: {path}\n")
                sys.exit()
            except OSError:
                self.environment.error(f"myshell: cannot read file: {path}\n")
                sys.exit()
        os.environ["shell"] = __file__
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTSTP, self.handle_sigtstp)

    async def execute(self, s: str):
        """处理单行命令输入"""
        s = s.strip()
        if s == "exit" or s.startswith("exit "):
            sys.exit()
        try:
            await self.job_manager.execute(s)
            await self.job_manager.wait()
        except ParsingError:
            self.environment.error("myshell: parsing error\n")

    async def run(self):
        """主函数"""
        if self.file is not None:
            for line in self.file:
                await self.execute(line)
        else:
            while True:
                s = await aioconsole.ainput(f"({os.getcwd()}) $ ")  # 需要异步的命令行读入
                await self.execute(s)


def main():
    app = App()
    app.bootstrap()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
