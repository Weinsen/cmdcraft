#!/usr/bin/env python3
"""Input related classes."""

import enum
import shlex


class InputState(enum.Enum):
    """Input typing state.

    This enumarator is used to indicate to the Completer the typing status. The list of
    available options is then considered.
    """

    EMPTY = enum.auto()
    TYPING_COMPLETE = enum.auto()
    TYPING_PARAMETER = enum.auto()
    TYPING_OPTION = enum.auto()
    TYPING_VALUE = enum.auto()
    TYPING_STRING = enum.auto()


class Input:
    """Prompt Input class.

    This class manages inputs data, handling token extraction and state analysis.
    """

    def __init__(self, input: str) -> None:
        """Input class initializer."""
        self._input = input
        self._tokens = []
        self._state = InputState.EMPTY

    @staticmethod
    def tokenize(input: str) -> list[str]:
        """Process an input into tokens.

        Within this context, tokens are units of data that are interpreted by the engine
        to execute a command. These tokens can be either (but not limited to) commands,
        arguments and options.

        Args:
            input (str): Raw prompted input.

        Returns:
            list[str]: List of input tokens.

        """
        tks = shlex.split(input.rstrip(), comments=True, posix=True)
        return tks

    def process(self) -> None:
        """Process an input."""
        try:
            self._tokens = self.tokenize(self._input)
        except ValueError:
            self._state = InputState.TYPING_STRING
            return

        if len(self._tokens) == 0 or not self._input:
            self._state = InputState.EMPTY
            return

        last_token = self._tokens[-1]
        if self._input.endswith(" "):
            self._state = InputState.TYPING_COMPLETE
        elif "=" in last_token:
            self._state = InputState.TYPING_VALUE
        elif last_token.startswith("--"):
            self._state = InputState.TYPING_OPTION
        else:
            self._state = InputState.TYPING_PARAMETER

    @property
    def position(self) -> int:
        """Returns the current position being typed."""
        if self._state in (InputState.TYPING_COMPLETE, InputState.EMPTY):
            return len(self._tokens)
        return len(self._tokens) - 1

    @property
    def tokens(self) -> list:
        """Returns a list of tokens of an Input.

        The Input must be previously proceded.
        """
        return self._tokens[:]

    @property
    def state(self) -> InputState:
        """Retuns the actual state of the Input."""
        return self._state
