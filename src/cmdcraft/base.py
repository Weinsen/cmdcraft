# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Base interpreter class."""

import asyncio
import os
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from inspect import cleandoc

from .command import Command
from .group import CommandGroup, split_command_path
from .input import Input


class BasePrompter(metaclass=ABCMeta):
    """Prompter basic command set.

    This class offers an operational command set to be embedded into the CLI
    interpreter.
    """

    def __init__(self) -> None:
        """Command Set initializer."""
        self._root_group = CommandGroup('root')
        self._commands: dict[str, Command | CommandGroup] = self._root_group.commands
        # Register default commands
        self.register_command(self.clear)
        self.register_command(self.history)
        self.register_command(self.load)
        self.register_command(self.quit)
        self.register_command(self.save)
        self.register_command(self.wait)

        # Register help command
        help_command = self.register_command(self.help)

        def get_funcs() -> list[str]:
            return self._root_group.command_paths(include_groups=True)

        help_command.parameter('command').set_dynamic_options(get_funcs)

        self._history: list[str] = []
        self._is_running: bool = False
        self._is_init: bool = False
        self._shutdown_requested: bool = False

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
        self._shutdown_requested = False

    @property
    def is_running(self) -> bool:
        """Returns if the execution loop is active.

        Returns:
            bool: True if the loop is active, False otherwise.

        """
        return self._is_running

    @property
    def shutdown_requested(self) -> bool:
        """Return whether a graceful shutdown was requested."""
        return self._shutdown_requested

    def request_shutdown(self) -> None:
        """Request a graceful shutdown."""
        if self._shutdown_requested:
            self.output("Forced shutdown requested.")
            raise SystemExit(130)

        self._shutdown_requested = True
        self._is_running = False
        self.output(
            "Graceful shutdown requested. Waiting for the current operation "
            "to finish. Press Ctrl-C again to force exit."
        )

    def register_command(
        self,
        command: Callable[..., object],
        alias: str | None = None,
    ) -> Command:
        """Register a command into the interpreter.

        Args:
            command (Callable[..., object]): Callable.
            alias (str | None, optional): Command alias. Defaults to None.

        Returns:
            Command: Registered command wrapper.

        """
        return self._root_group.register_command(command, alias)

    def register_group(
        self, name: str, alias: str | None = None, doc: str | None = None
    ) -> CommandGroup:
        """Register a command group into the interpreter.

        Args:
            name (str): Group name.
            alias (str | None, optional): Group alias or path. Defaults to None.
            doc (str | None, optional): Group documentation. Defaults to None.

        Returns:
            CommandGroup: Registered command group.

        """
        return self._root_group.register_group(name, alias=alias, doc=doc)

    @property
    def commands(self) -> dict[str, Command | CommandGroup]:
        """Return the available top-level commands and groups.

        Returns:
            dict[str, Command | CommandGroup]: Top-level command and group
                dictionary.

        """
        return self._commands

    def _resolve_command_path(
        self, tokens: list[str]
    ) -> tuple[Command | CommandGroup | None, int]:
        """Resolve a command path from the current registry."""
        return self._root_group.resolve(tokens)

    def _command_paths(self, include_groups: bool = False) -> list[str]:
        """Return all registered command paths."""
        return self._root_group.command_paths(include_groups=include_groups)

    def _format_group_help(self, group_path: str, group: CommandGroup) -> str:
        """Build help text for a command group."""
        lines = []
        if group.__doc__:
            lines.append(cleandoc(group.__doc__))
        else:
            lines.append(f'Command group: {group_path}')

        lines.append('')
        lines.append('Available commands:')
        for name in group.commands:
            lines.append(f'- {name}')
        return '\n'.join(lines)

    async def interpret(self, cmdline: str) -> None:
        """Interpret user input.

        This method is used to parse input commands, handling eventual failures
        and raised exceptions.

        Args:
            cmdline (str): Input command as single string line.

        Returns:
            None: This coroutine does not return a value.

        """
        command_path = 'help'
        try:
            prompt_input = Input(cmdline)
            prompt_input.process()
            if len(prompt_input.tokens) < 1:
                return
            command_path = prompt_input.tokens[0]
            cmd, consumed = self._resolve_command_path(prompt_input.tokens)
            if cmd is None:
                self.output(f'Unknown command: {prompt_input.tokens[0]}')
                await self.help()
                return

            command_path = ' '.join(prompt_input.tokens[:consumed])
            if isinstance(cmd, CommandGroup):
                if consumed == len(prompt_input.tokens):
                    await self.help(command_path)
                else:
                    unknown = ' '.join(prompt_input.tokens[: consumed + 1])
                    self.output(f'Unknown command: {unknown}')
                    await self.help(command_path)
                return

            args = prompt_input.tokens[consumed:]
            if cmd.alias == 'help' and consumed == 1 and len(args) > 1:
                args = [' '.join(args)]

            await cmd.eval(*args)
        except TypeError as e:
            await self.help(command_path)
            self.output(e)
        except Exception as e:
            self.output(e)

    async def help(self, command: str = 'help') -> None:
        """Show Cmdcraft interpreter help.

        The interpreter receives instructions from the standard input (stdin) to
        dynamically execute operations on running services.

        For further help, type the command `help [command [subcommand]]`.

        Args:
            command (str, optional): Command path to describe. Defaults to
                "help".

        Returns:
            None: This coroutine does not return a value.

        """
        help_text = cleandoc(self.help.__doc__ or '').split('\n\nArgs:\n', 1)[0]
        tokens = split_command_path(command) if command.strip() else ['help']
        if tokens == ['help']:
            self.output(help_text)
            self.output('')
            return

        cmd, consumed = self._resolve_command_path(tokens)
        if isinstance(cmd, CommandGroup) and consumed == len(tokens):
            self.output(self._format_group_help(command, cmd))
        elif isinstance(cmd, Command):
            self.output(cleandoc(cmd.__doc__))
        else:
            self.output(help_text)
        self.output('')

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
