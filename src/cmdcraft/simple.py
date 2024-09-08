#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple prompt interpreter."""

from __future__ import annotations

import asyncio
import sys

from .base import BaseInterpreter


class SimpleInterpreter(BaseInterpreter):
    """CLI Interpreter class.

    This class is responsible for the CLI principal operations, parsing input
    data and calling the respectives actions.
    """

    def __init__(self, *, stream: any = sys.stdin) -> None:
        """Construct the interpreter object.

        Args:
            stream (any, optional): Input stream. Defaults to sys.stdin.
        """
        super().__init__()
        self._stream = stream
        self._reader: asyncio.StreamReader | None = None
        self._protocol: asyncio.StreamReaderProtocol | None = None

    async def init(self) -> None:
        """Init the interpreter object."""
        await super().init()
        loop = asyncio.get_event_loop()
        self._reader = asyncio.StreamReader()
        self._protocol = asyncio.StreamReaderProtocol(self._reader)
        await loop.connect_read_pipe(lambda: self._protocol, self._stream)

    async def run(self) -> None:
        """Main Interpreter running loop."""
        self._is_running = True
        await self.interpret("help")
        while self.is_running:
            print("\n> ", end="")
            cmdline = await self._reader.read(256)
            cmdline = cmdline.decode().rstrip()
            if not cmdline:
                continue
            self._history.append(cmdline)
            await self.interpret(cmdline)

    def output(self, *args) -> None:
        """Output method."""
        print(*args)
