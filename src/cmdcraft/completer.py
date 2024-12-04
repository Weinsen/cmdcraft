#!/usr/bin/env python3
"""Prompt completer class."""

from __future__ import annotations

from typing import Iterable

from prompt_toolkit.completion import (
    CompleteEvent,
    Completion,
    FuzzyWordCompleter,
    NestedCompleter,
)
from prompt_toolkit.document import Document

from cmdcraft.command import Command
from cmdcraft.input import Input, InputState


class CommandCompleter(NestedCompleter):
    """Prompt Completer class."""

    def __init__(self, command: Command, ignore_case: bool = True) -> None:
        """CommandCompleter constructor.

        Args:
            command (Command): Command which will be used as base.
            ignore_case (bool, optional): Sets if input should be case-sensitive
                or not. Defaults to True.

        """
        super().__init__([], ignore_case)
        self._command = command

    def _get_par_completions(
        self, input: Input, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Get parameter completions.

        Args:
            input (Input): Prompt input.
            document (Document): Current document object.
            complete_event (CompleteEvent): Completion event.

        Returns:
            Iterable[Completion]: List of Completions for current prompt.

        """
        pars = list(self._command._positional.keys())
        idx = pars[input.position]
        par = self._command._positional[idx]
        completer = FuzzyWordCompleter(list(par.options))
        return completer.get_completions(document, complete_event)

    def _get_opt_completions(
        self, _: str, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Get parameter completions.

        Args:
            prompt (str): Prompt input.
            document (Document): Current document object.
            complete_event (CompleteEvent): Completion event.

        Returns:
            Iterable[Completion]: List of Completions for current prompt.

        """
        pars = [f"--{x}" for x in self._command.keyword_parameters]
        completer = FuzzyWordCompleter(list(pars))
        return completer.get_completions(document, complete_event)

    def _get_value_completions(
        self, prompt: str, _: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Get argument completions.

        Args:
            prompt (str): Prompt input.
            document (Document): Current document object.
            complete_event (CompleteEvent): Completion event.

        Returns:
            Iterable[Completion]: List of Completions for current prompt.

        """
        (par, arg) = prompt.lstrip("--").split("=")
        if par not in self._command._pars:
            return ()
        vs = self._command._pars[par].options
        if vs is None:
            return ()
        completer = FuzzyWordCompleter(vs)
        doc = Document(arg, -len(arg) - 2)
        return completer.get_completions(doc, complete_event)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Get list of completions for current input.

        Args:
            document (Document): Current document object.
            complete_event (CompleteEvent): Completion event.

        Returns:
            Iterable[Completion]: List of Completions for current prompt.

        """
        try:
            input = Input(document.text)
            input.process()
            if input.position < len(self._command._positional):
                return self._get_par_completions(input, document, complete_event)
            elif input.state in (InputState.TYPING_OPTION, InputState.TYPING_COMPLETE):
                return self._get_opt_completions("", document, complete_event)
            elif input.state == InputState.TYPING_VALUE:
                word = input.tokens[-1]
                return self._get_value_completions(word, document, complete_event)
            else:
                return ()
        except ValueError:  # TODO: improve open quote handling
            return ()
