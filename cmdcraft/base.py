#!/usr/bin/env python
# *****************************************************************************
# Copyright (c) 2024, Antonio Mario Weinsen Junior <weinsen.mbed@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

from __future__ import annotations

import asyncio
import os
from inspect import cleandoc
from inspect import getfullargspec
from typing import get_type_hints

class BaseInterpreter:
    """Interpreter basic command set.

    This class offers an operational command set to be embedded into the CLI
    interpreter.
    """

    def __init__(self) -> None:
        """Command Set initializer."""
        self._commands: dict[str, callable] = {
            'clear': self.clear,
            'help': self.help,
            'history': self.history,
            'load': self.load,
            'quit': self.quit,
            'save': self.save,
            'wait': self.wait
        }
        self._history = []
        self._is_running : bool = False

    @property
    def is_running(self) -> bool:
        """Returns if the execution loop is active.

        Returns:
            bool: True if the loop is active, False otherwise.
        """
        return self._is_running

    def register_command(self, name: str, command: callable) -> None:
        """Registers a command into the interpreter.

        Args:
            name (str): Command name, alias.
            command (callable): Callable object.
        """
        self._commands[name] = command

    def show_commands(self) -> None:
        """Shows available commands."""
        cmds = ', '.join(list(self._commands))
        print(f'Available commands: {cmds}')

    def _cast_call(self, f: callable, *args: list,
                  **kwargs: dict) -> asyncio.Future:
        """Calls the callable casting arguments to the parameter list.

        This method may be used to ensured that the argument type matches the
        type expect by the callable signature specified with annotations.

        Args:
            f (callable): Callable object.

        Returns:
            asyncio.Future: Awaitable object.
        """
        anns = get_type_hints(f)
        arglist = getfullargspec(f).args
        if 'self' in arglist:
            arglist.remove('self')

        targs = []

        for k, v in zip(arglist, args):
            if k in anns:
                vartype = anns.get(k)
                targs.append(vartype(v))
            else:
                targs.append(v)

        if len(targs) < len(args):
            targs.extend(args[len(targs):])

        for k, v in kwargs.items():
            if k in anns:
                vartype = anns.get(k)
                kwargs[k] = vartype(v)
            else:
                kwargs[k] = v

        return f(*targs, **kwargs)

    async def interpret(self, cmdline: str) -> None:
        """Main Interpreter method for parsing commands.

        This method is used to parse input commands, handling eventual failures
        and raised exceptions.

        Args:
            input (str): Input command as single string line.
        """
        cmdline = cmdline.split()
        args = [a for a in cmdline if '=' not in a]
        kwargs = dict([a.split('=') for a in cmdline if '=' in a])
        try:
            cmd = self._commands.get(args[0], None)
            if args[0] == 'help':
                if len(args) > 1:
                    cmd = self._commands.get(args[1], None)
                await self.help(cmd)
            elif cmd is None:
                print(f'Invalid command `{args[0]}`!')
                self.show_commands()
            else:
                await self._cast_call(cmd, *args[1:], **kwargs)
        except TypeError as e:
            await self.help(cmd)
            print(e)
        except Exception as e:
            print(e)

    async def help(self, command: callable | None = None) -> None:
        """ICP Mockup interpreter help.

        The interpreter receives instructions from the standard input (stdin) to
        dynamically execute operations on running services.

        For further help, type the command `help [command]`.
        """
        if command is None or command == self.help:
            print(cleandoc(self.help.__doc__))
            self.show_commands()
        else:
            print(cleandoc(command.__doc__))

    async def clear(self) -> None:
        """Clears both command history and screen."""
        self._history.clear()
        os.system('clear')

    async def history(self) -> None:
        """Shows command history."""
        print('\n'.join(self._history))

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
            filepath = os.path.join('routines', filepath)

        with open(filepath, 'w', encoding='utf-8') as f:
            script = [
                x + '\n'
                for x in self._history
                if not x.startswith(('save', 'history', 'help'))
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
            filepath = os.path.join('routines', filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith(('save', 'history', 'help')):
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