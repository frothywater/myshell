#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from myshell.manager import JobManager


class Environment:
    """程序基本环境

    包含了默认输入输出流和事务管理器"""

    def __init__(self):
        self.in_ = sys.stdin
        self.out = sys.stdout
        self.err = sys.stderr
        self.job_manager = JobManager(self)  # 事务管理器

    def write(self, s: str):
        """写入到标准输出流"""
        self.out.write(s)

    def error(self, s: str):
        """写入到标准错误流"""
        self.err.write(s)
