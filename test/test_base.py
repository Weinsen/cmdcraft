# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Tests for BasePrompter."""

import asyncio

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
