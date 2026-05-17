# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Tests for BasePrompter."""

import asyncio
from enum import Enum

from cmdcraft.base import BasePrompter


class _DummyPrompter(BasePrompter):
    def __init__(self) -> None:
        self.outputs = []
        super().__init__()

    def output(self, *args) -> None:
        self.outputs.append(" ".join(str(arg) for arg in args))


def test_interpret_unknown_command():
    """Test handling of unknown commands."""
    prompt = _DummyPrompter()

    asyncio.run(prompt.interpret("missing"))

    assert prompt.outputs[0] == "Unknown command: missing"
    assert "Show Cmdcraft interpreter help." in prompt.outputs[1]


def test_request_shutdown_escalates_on_second_call():
    """Test graceful then forced shutdown requests."""
    prompt = _DummyPrompter()
    prompt._is_running = True

    prompt.request_shutdown()
    assert prompt.shutdown_requested is True
    assert prompt.is_running is False
    assert prompt.outputs[-1] == (
        "Graceful shutdown requested. Waiting for the current operation to "
        "finish. Press Ctrl-C again to force exit."
    )

    try:
        prompt.request_shutdown()
    except SystemExit as exc:
        assert exc.code == 130
    else:
        assert False, "Expected a forced shutdown to raise SystemExit"

    assert prompt.outputs[-1] == "Forced shutdown requested."


def test_interpret_positional_enum_assignment_hint():
    """Test a readable hint for mistaken named positional enum syntax."""

    class EnumTest(Enum):
        A = 1
        B = 2

    async def test_input(a: EnumTest) -> None:
        return None

    prompt = _DummyPrompter()
    prompt.register_command(test_input)

    asyncio.run(prompt.interpret("test_input a=A"))

    assert prompt.outputs == ["Parameter 'a' is positional. Use 'A' instead of 'a=A'."]
