#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prompt Interpreter."""

from __future__ import annotations

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter

from cmdcraft import BaseInterpreter

from .completer import CommandCompleter


class Interpreter(BaseInterpreter):
    """Prompt Interpreter class."""

    def __init__(self) -> None:
        """Construct the interpreter object."""
        super().__init__()
        self._session = PromptSession()

    async def init(self) -> None:
        """Init the interpreter object."""
        await super().init()

    def completer(self) -> None:
        """Process interpreter completer."""
        cmds = {}
        for name, cmd in self._commands.items():
            if name == "help":
                continue
            cmds[name] = CommandCompleter(cmd)
        return NestedCompleter(cmds)

    async def run(self) -> None:
        """Main Interpreter running loop."""
        await super().run()
        self._is_running = True
        await self.interpret("help")
        while self.is_running:
            cmdline = await self._session.prompt_async("> ", completer=self.completer())
            cmdline = cmdline.rstrip()
            if not cmdline:
                continue
            self._history.append(cmdline)
            await self.interpret(cmdline)

    def output(self, *args) -> None:
        """Output command."""
        print(*args)
