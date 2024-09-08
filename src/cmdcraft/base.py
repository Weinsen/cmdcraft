#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base interpreter class."""

import asyncio
import os
import shlex
from abc import ABCMeta, abstractmethod
from inspect import cleandoc

from .method import Method


class BaseInterpreter(metaclass=ABCMeta):
    """Interpreter basic command set.

    This class offers an operational command set to be embedded into the CLI
    interpreter.
    """

    def __init__(self) -> None:
        """Command Set initializer."""
        self._commands: dict[str, Method] = {}
        self.register_command(self.clear)
        self.register_command(self.help)
        self.register_command(self.history)
        self.register_command(self.load)
        self.register_command(self.quit)
        self.register_command(self.save)
        self.register_command(self.wait)
        self._history = []
        self._is_running: bool = False

    async def init(self) -> None:
        """Init the interpreter object."""
        for c in self._commands.values():
            c.process()

    @abstractmethod
    def output(self, *args) -> None:
        """Output method."""

    @abstractmethod
    async def run(self) -> None:
        """Main Interpreter running loop."""

    @property
    def is_running(self) -> bool:
        """Returns if the execution loop is active.

        Returns:
            bool: True if the loop is active, False otherwise.
        """
        return self._is_running

    def register_command(self, command: callable, alias: str | None = None) -> None:
        """Register a command into the interpreter.

        Args:
            command (callable): Callable.
            alias (str | None, optional): Command alias. Defaults to None.
        """
        m = Method(command, alias)
        self._commands[m.alias] = m

    @property
    def commands(self) -> dict:
        """Return the available commands.

        Returns:
            dict: Commands dictionary.
        """
        return self._commands

    def show_commands(self) -> None:
        """Shows available commands."""
        cmds = ", ".join(list(self._commands))
        self.output(f"Available commands: {cmds}")

    async def interpret(self, cmdline: str) -> None:
        """Main Interpreter method for parsing commands.

        This method is used to parse input commands, handling eventual failures
        and raised exceptions.

        Args:
            cmdline (str): Input command as single string line.
        """
        try:
            args = shlex.split(cmdline, comments=True, posix=True)
            cmd = self._commands.get(args[0], None)
            if args[0] == "help":
                if len(args) > 1:
                    cmd = self._commands.get(args[1], None)
                await self.help(cmd)
            elif cmd is None:
                self.output(f"Invalid command `{args[0]}`!")
                self.show_commands()
            else:
                await cmd.eval(*args[1:])
        except TypeError as e:
            await self.help(cmd)
            self.output(e)
        except Exception as e:
            self.output(e)

    async def help(self, command: str = None) -> None:
        """ICP Mockup interpreter help.

        The interpreter receives instructions from the standard input (stdin) to
        dynamically execute operations on running services.

        For further help, type the command `help [command]`.
        """
        self.output(cleandoc(command.__doc__))

    async def clear(self) -> None:
        """Clears both command history and screen."""
        self._history.clear()
        os.system("clear")

    async def history(self) -> None:
        """Shows command history."""
        self.output("\n".join(self._history))

    async def save(self, file: str) -> None:
        """Saves the current command history to a file.

        This may be used to save the current command history as an external file
        for posterior loading.

        If the provided file path is not absolute, the contents will be saved
        into `routines` folder.

        Args:
            file (str): Filename.
        """
        filepath = os.path.join(file)
        if not os.path.isabs(file):
            filepath = os.path.join("routines", filepath)

        with open(filepath, "w", encoding="utf-8") as f:
            script = [
                x + "\n"
                for x in self._history
                if not x.startswith(("save", "history", "help"))
            ]
            for line in script:
                f.write(line)

    async def load(self, file: str) -> None:
        """Loads a command file.

        This may be used to recover previously saved command history into the
        current execution list.

        If the provided file path is not absolute, the contents will be loaded
        from `routines` folder.

        Args:
            file (str): Filename.
        """
        filepath = os.path.join(file)
        if not os.path.isabs(file):
            filepath = os.path.join("routines", filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(("save", "history", "help")):
                    continue
                await self.interpret(line.rstrip())

    async def wait(self, delay: float) -> None:
        """Blocks the execution list for given time.

        Args:
            delay (float): Blocks execution for given time in seconds.
        """
        await asyncio.sleep(float(delay))

    async def quit(self) -> None:
        """Stops the execution loop.

        This method calls for a graceful exit, waiting the current scheduled
        commands to execute.
        """
        self._is_running = False
