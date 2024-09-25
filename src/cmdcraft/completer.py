#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prompt completer class."""

from __future__ import annotations

import shlex
from typing import Iterable

from prompt_toolkit.completion import (
    CompleteEvent,
    Completion,
    FuzzyWordCompleter,
    NestedCompleter,
)
from prompt_toolkit.document import Document

from cmdcraft.command import Command


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

    def _get_pcompletions(
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
        pars = self._command.list_parameters()
        completer = FuzzyWordCompleter(list(pars))
        return completer.get_completions(document, complete_event)

    def _get_acompletions(
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
        (par, arg) = prompt.split("=")
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
        prompt = shlex.split(document.text + "_")
        if len(prompt) < 1:
            return ()
        word = prompt[-1]
        if word == "_":
            return self._get_pcompletions(word, document, complete_event)
        if "=" in word:
            return self._get_acompletions(word, document, complete_event)
        return self._get_pcompletions(word, document, complete_event)
