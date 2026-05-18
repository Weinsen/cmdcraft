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

import pytest

from cmdcraft.base import BasePrompter
from cmdcraft.group import CommandGroup


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


def test_interpret_type_error_shows_command_help():
    """Test TypeError handling shows the failing command help text."""

    async def test_input(required: str) -> None:
        """Specific command help."""
        return None

    prompt = _DummyPrompter()
    prompt.register_command(test_input)

    asyncio.run(prompt.interpret("test_input"))

    assert prompt.outputs[0] == "Specific command help."
    assert prompt.outputs[1] == ""
    assert "missing 1 required positional argument" in prompt.outputs[2]


def test_interpret_grouped_command_alias_path():
    """Test grouped command aliases resolve as command paths."""

    async def motor_start() -> None:
        prompt.output("motor started")

    prompt = _DummyPrompter()
    prompt.register_command(motor_start, alias="motor start")

    asyncio.run(prompt.interpret("motor start"))

    assert prompt.outputs == ["motor started"]


def test_interpret_nested_registered_groups():
    """Test nested command groups resolve commands."""

    async def start() -> None:
        prompt.output("axis started")

    prompt = _DummyPrompter()
    axis = prompt.register_group("motor axis")
    axis.register_command(start)

    asyncio.run(prompt.interpret("motor axis start"))

    assert prompt.outputs == ["axis started"]


def test_grouped_command_type_error_shows_nested_command_help():
    """Test grouped command failures show the nested command help."""

    async def motor_start(speed: str) -> None:
        """Motor start help."""
        return None

    prompt = _DummyPrompter()
    prompt.register_command(motor_start, alias="motor start")

    asyncio.run(prompt.interpret("motor start"))

    assert prompt.outputs[0] == "Motor start help."
    assert prompt.outputs[1] == ""
    assert "missing 1 required positional argument" in prompt.outputs[2]


def test_help_accepts_unquoted_grouped_command_path():
    """Test help accepts grouped command paths without quoting."""

    async def motor_start() -> None:
        """Motor start help."""
        return None

    prompt = _DummyPrompter()
    prompt.register_command(motor_start, alias="motor start")

    asyncio.run(prompt.interpret("help motor start"))

    assert prompt.outputs == ["Motor start help.", ""]


def test_help_command_hides_api_doc_sections():
    """Test interpreter help does not expose API doc sections."""
    prompt = _DummyPrompter()

    asyncio.run(prompt.interpret("help"))

    assert prompt.outputs[0].startswith("Show Cmdcraft interpreter help.")
    assert "Args:" not in prompt.outputs[0]
    assert "Returns:" not in prompt.outputs[0]
    assert prompt.outputs[1] == ""


def test_register_group_path_uses_leaf_group_name():
    """Test grouped paths register the leaf group at the leaf level."""
    prompt = _DummyPrompter()

    axis = prompt.register_group("motor axis")
    motor = prompt.commands["motor"]

    assert isinstance(motor, CommandGroup)
    assert axis.name == "axis"
    assert axis.alias == "axis"
    assert motor.commands["axis"] is axis


def test_register_command_path_uses_leaf_command_alias():
    """Test grouped command paths register the command at the leaf level."""

    async def command_input() -> None:
        return None

    prompt = _DummyPrompter()
    command = prompt.register_command(command_input, alias="motor axis home")
    motor = prompt.commands["motor"]
    axis = motor.commands["axis"]

    assert isinstance(motor, CommandGroup)
    assert isinstance(axis, CommandGroup)
    assert command.alias == "home"
    assert axis.commands["home"] is command


def test_register_group_paths_merge_same_parent_group():
    """Test sibling group paths reuse the same parent group."""
    prompt = _DummyPrompter()

    axis = prompt.register_group("motor axis")
    sensor = prompt.register_group("motor sensor")
    motor = prompt.commands["motor"]

    assert isinstance(motor, CommandGroup)
    assert motor.commands["axis"] is axis
    assert motor.commands["sensor"] is sensor


def test_register_command_raises_for_duplicate_command_name():
    """Test duplicate command registrations raise an exception."""

    async def start() -> None:
        return None

    prompt = _DummyPrompter()
    prompt.register_command(start, alias="motor start")

    with pytest.raises(ValueError, match="already registered"):
        prompt.register_command(start, alias="motor start")


def test_register_command_raises_for_existing_group_name():
    """Test command registrations cannot replace existing groups."""

    async def axis() -> None:
        return None

    prompt = _DummyPrompter()
    prompt.register_group("motor axis")

    with pytest.raises(ValueError, match="already registered"):
        prompt.register_command(axis, alias="motor axis")


def test_register_group_raises_for_existing_command_name():
    """Test group registrations cannot replace existing commands."""

    async def axis() -> None:
        return None

    prompt = _DummyPrompter()
    prompt.register_command(axis, alias="motor axis")

    with pytest.raises(ValueError, match="already registered"):
        prompt.register_group("motor axis")
