#!/usr/bin/env python3
"""Base interpreter class."""

import asyncio
import os
from abc import ABCMeta, abstractmethod
from inspect import cleandoc

from .command import Command
from .input import Input


class BasePrompter(metaclass=ABCMeta):
    """Prompter basic command set.

    This class offers an operational command set to be embedded into the CLI
    interpreter.
    """

    def __init__(self) -> None:
        """Command Set initializer."""
        self._commands: dict[str, Command] = {}
        # Register default commands
        self.register_command(self.clear)
        self.register_command(self.history)
        self.register_command(self.load)
        self.register_command(self.quit)
        self.register_command(self.save)
        self.register_command(self.wait)

        # Register help command
        help = self.register_command(self.help)

        def get_funcs() -> list[str]:
            return list(self._commands)

        help.parameter("command").set_dynamic_options(get_funcs)

        self._history = []
        self._is_running: bool = False
        self._is_init: bool = False

    async def init(self) -> None:
        """Init the interpreter object."""
        self._is_init = True

    @abstractmethod
    def output(self, *args) -> None:
        """Output command."""

    async def run(self) -> None:
        """Run Prompter main loop."""
        if not self._is_init:
            await self.init()

    @property
    def is_running(self) -> bool:
        """Returns if the execution loop is active.

        Returns:
            bool: True if the loop is active, False otherwise.

        """
        return self._is_running

    def register_command(self, command: callable, alias: str | None = None) -> Command:
        """Register a command into the interpreter.

        Args:
            command (callable): Callable.
            alias (str | None, optional): Command alias. Defaults to None.

        """
        m = Command(command, alias)
        self._commands[m.alias] = m
        m.process()
        return m

    @property
    def commands(self) -> dict:
        """Return the available commands.

        Returns:
            dict: Commands dictionary.

        """
        return self._commands

    async def interpret(self, cmdline: str) -> None:
        """Interpret user input.

        This method is used to parse input commands, handling eventual failures
        and raised exceptions.

        Args:
            cmdline (str): Input command as single string line.

        """
        try:
            input = Input(cmdline)
            input.process()
            if len(input.tokens) < 1:
                return
            cmd = self._commands.get(input.tokens[0], None)
            await cmd.eval(*input.tokens[1:])
        except TypeError as e:
            await self.help(cmd)
            self.output(e)
        except Exception as e:
            self.output(e)

    async def help(self, command: str = "help") -> None:
        """Show Cmdcraft interpreter help.

        The interpreter receives instructions from the standard input (stdin) to
        dynamically execute operations on running services.

        For further help, type the command `help [command]`.
        """
        cmd = self._commands.get(command, None)
        if cmd:
            self.output(cleandoc(cmd.__doc__))
        else:
            self.output(cleandoc(self.help.__doc__))
        self.output("")

    async def clear(self) -> None:
        """Clear both command history and screen."""
        self._history.clear()
        os.system("clear")

    async def history(self) -> None:
        """Show command history."""
        self.output("\n".join(self._history))

    async def save(self, file: str) -> None:
        """Save the current command history to a file.

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
        """Load a command file.

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

        with open(filepath, encoding="utf-8") as f:
            for line in f:
                if line.startswith(("save", "history", "help")):
                    continue
                await self.interpret(line.rstrip())

    async def wait(self, delay: float) -> None:
        """Block the execution list for given time.

        Args:
            delay (float): Blocks execution for given time in seconds.

        """
        await asyncio.sleep(float(delay))

    async def quit(self) -> None:
        """Stop the execution loop.

        This method calls for a graceful exit, waiting the current scheduled
        commands to execute.
        """
        self._is_running = False
