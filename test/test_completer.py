#!/usr/bin/env python3

from enum import Enum

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document

from cmdcraft.command import Command
from cmdcraft.completer import CommandCompleter


class EnumTest(Enum):
    A = 1
    B = 2


async def _test_input(a: EnumTest, *, prompt: str) -> None:
    return None


def _dynamic_options() -> list[str]:
    return ["alpha", "beta"]


def _build_completer() -> CommandCompleter:
    cmd = Command(_test_input)
    cmd.process()
    cmd.parameter("prompt").set_dynamic_options(_dynamic_options)
    return CommandCompleter(cmd)


def test_keyword_value_completion_uses_dynamic_options():
    """Test keyword value completion with dynamic options."""
    completer = _build_completer()

    completions = [
        completion.text
        for completion in completer.get_completions(
            Document("test_input --prompt="), CompleteEvent()
        )
    ]

    assert completions == ["alpha", "beta"]


def test_positional_value_assignment_has_no_completions():
    """Test positional parameters do not get keyword-style value completion."""
    completer = _build_completer()

    completions = [
        completion.text
        for completion in completer.get_completions(
            Document("test_input a="), CompleteEvent()
        )
    ]

    assert completions == []