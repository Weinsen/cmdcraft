#!/usr/bin/env python3
"""Input class."""

import enum
import shlex


class InputState(enum.Enum):
    TYPING_PARAMETER = enum.auto()
    TYPING_ARGUMENT = enum.auto()
    TYPING_STRING = enum.auto()


class Input:
    def __init__(self, input: str) -> None:
        self._input = input
        self._tokens = []
        self._state = InputState.TYPING_PARAMETER

    @staticmethod
    def tokenize(input: str) -> list[str]:
        tks = shlex.split(input.rstrip(), comments=True, posix=True)
        # tks = [x.split('=', 1) if '=' in x else x for x in tks]
        # tks = [x[0] if len(x) == 1 else {x[0]: x[1]} for x in tks]
        return tks

    def process(self) -> None:
        if self._input.endswith(" "):
            self._state = InputState.TYPING_PARAMETER
        elif self._input.endswith("="):
            self._state = InputState.TYPING_ARGUMENT
        try:
            self._tokens = self.tokenize(self._input)
        except ValueError:
            self._state = InputState.TYPING_STRING

    @property
    def tokens(self) -> list:
        return self._tokens[:]

    @property
    def state(self) -> InputState:
        return self._state
