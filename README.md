# myshell

一个 Bash Shell 的重新实现，仅仅包含最简单的基本功能。

# 项目结构

`myshell` 为本项目的父包，其子模块包含了本程序的核心功能：

- `myshell.main` 是程序起始点，定义了顶层类 `App`。
- `myshell.environment` 定义了程序基本环境类 `Environment`，包含了默认输入输出流和事务管理器。
- `myshell.manager` 定义了事务管理器 `JobManager`，用以调度前台和后台事务。
- `myshell.job` 定义了事务类 `Job`，用以调度单个事务。
- `myshell.pipeline` 定义了类 `Pipeline`，用以处理一个事务中命令之间的管道。
- `myshell.instruction` 定义了类 `Instruction`，用以处理单个命令的重定向。
- `myshell.context` 定义了类 `Context`，包含了单个命令执行时的上下文，输入输出流和整个程序的环境。
- `myshell.command` 定义了抽象基类 `Command`，所有命令类由此继承。

`myshell.commands` 包含了本程序定义的命令类。

# 运行

使用以下命令运行 `myshell`：

```bash
python myshell/main.py
```

或使用以下命令向其输入一个 Shell 文件：

```bash
python myshell/main.py example.sh
```

# 支持的命令

# 用户手册

请参阅 [manual.md](doc/manual.md)。

# 参考资料

仅列出一部分文档：

1. [os — Miscellaneous operating system interfaces — Python 3.9.6 documentation](https://docs.python.org/3/library/os.html#os.execv)
2. [sys — System-specific parameters and functions — Python 3.9.6 documentation](https://docs.python.org/3/library/sys.html)
3. [asyncio — Asynchronous I/O — Python 3.9.6 documentation](https://docs.python.org/3/library/asyncio.html)
4. [Coroutines and Tasks — Python 3.9.6 documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio-awaitables)
5. [Subprocesses — Python 3.9.6 documentation](https://docs.python.org/3/library/asyncio-subprocess.html)
6. [Welcome to mypy documentation! — Mypy 0.910 documentation](https://mypy.readthedocs.io/en/stable/)
