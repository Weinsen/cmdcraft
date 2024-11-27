#!/usr/bin/env python3
"""Prompt Prompter."""

from __future__ import annotations

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter

from cmdcraft import BasePrompter

from .completer import CommandCompleter


class Prompter(BasePrompter):
    """Prompt Prompter class."""

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
            cmds[name] = CommandCompleter(cmd)
        return NestedCompleter(cmds)

    async def run(self) -> None:
        """Run Prompter main loop."""
        await super().run()
        self._is_running = True
        await self.interpret("help")
        while self.is_running:
            cmdline = await self._session.prompt_async("> ", completer=self.completer())
            self._history.append(cmdline)
            await self.interpret(cmdline)

    def output(self, *args) -> None:
        """Output command."""
        print(*args)
