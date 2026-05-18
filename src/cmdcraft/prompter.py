# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Prompt prompter implementation."""

from __future__ import annotations

import signal

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter

from cmdcraft import BasePrompter

from .command import Command
from .completer import CommandCompleter
from .group import CommandGroup


class Prompter(BasePrompter):
    """Prompt-toolkit powered prompter."""

    def __init__(self) -> None:
        """Construct the interpreter object.

        Returns:
            None: This constructor does not return a value.

        """
        super().__init__()
        self._session = PromptSession()
        self._previous_sigint_handler = None

    async def init(self) -> None:
        """Initialize the interpreter object.

        Returns:
            None: This coroutine does not return a value.

        """
        await super().init()

    def _completion_tree(
        self,
        commands: dict[str, Command | CommandGroup],
    ) -> dict[str, object]:
        """Build the nested completion tree for commands and groups."""
        items: dict[str, object] = {}
        for name, cmd in commands.items():
            if isinstance(cmd, CommandGroup):
                items[name] = self._completion_tree(cmd.commands)
            else:
                items[name] = CommandCompleter(cmd)
        return items

    def completer(self) -> NestedCompleter:
        """Process the interpreter completer.

        Returns:
            NestedCompleter: Prompt completer for commands, groups, and parameters.

        """
        return NestedCompleter.from_nested_dict(self._completion_tree(self._commands))

    def _has_active_prompt(self) -> bool:
        """Return whether a prompt_toolkit application is running."""
        app = self._session.app
        if app is None:
            return False
        future = getattr(app, 'future', None)
        return (
            getattr(app, 'is_running', False)
            and future is not None
            and not future.done()
        )

    def _exit_active_prompt(self) -> None:
        """Exit the active prompt without raising a traceback."""
        if self._has_active_prompt():
            self._session.app.exit(result='')

    def _handle_sigint(self, _: int, __) -> None:
        """Handle Ctrl-C with graceful-then-force semantics."""
        self._exit_active_prompt()
        self.request_shutdown()

    def _handle_runtime_interrupt(self) -> None:
        """Handle a KeyboardInterrupt raised inside the runtime loop."""
        if self.shutdown_requested:
            raise SystemExit(130) from None

        self.request_shutdown()

    async def run(self) -> None:
        """Run the prompter main loop.

        Returns:
            None: This coroutine does not return a value.

        """
        await super().run()
        self._is_running = True
        self._previous_sigint_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._handle_sigint)

        try:
            await self.interpret('help')
            while self.is_running:
                try:
                    cmdline = await self._session.prompt_async(
                        '> ',
                        completer=self.completer(),
                        handle_sigint=False,
                    )
                    if self.shutdown_requested:
                        break

                    self._history.append(cmdline)
                    await self.interpret(cmdline)
                except KeyboardInterrupt:
                    self._handle_runtime_interrupt()
                    break
        finally:
            if self._previous_sigint_handler is not None:
                signal.signal(signal.SIGINT, self._previous_sigint_handler)
                self._previous_sigint_handler = None

    def output(self, *args) -> None:
        """Output prompt results.

        Args:
            *args: Values to print.

        Returns:
            None: This method does not return a value.

        """
        print(*args)
