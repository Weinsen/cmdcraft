# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Tests for Prompter."""

import asyncio

import pytest
from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document

from cmdcraft.prompter import Prompter


class _DummyPrompter(Prompter):
    def __init__(self) -> None:
        self.outputs = []
        super().__init__()

    def output(self, *args) -> None:
        self.outputs.append(" ".join(str(arg) for arg in args))


class _FakeFuture:
    def __init__(self, done: bool = False) -> None:
        self._done = done

    def done(self) -> bool:
        return self._done


class _FakeApp:
    def __init__(self, running: bool = True) -> None:
        self.is_running = running
        self.future = _FakeFuture(done=not running)
        self.exit_calls = []

    def exit(self, result=None, exception=None, style: str = "") -> None:
        self.exit_calls.append(
            {"result": result, "exception": exception, "style": style}
        )
        self.is_running = False
        self.future = _FakeFuture(done=True)


class _FakeSession:
    def __init__(self, app: _FakeApp) -> None:
        self.app = app


class _GracefulInterruptSession(_FakeSession):
    def __init__(self, prompt: Prompter, app: _FakeApp) -> None:
        super().__init__(app)
        self._prompt = prompt

    async def prompt_async(self, *args, **kwargs) -> str:
        self._prompt._handle_sigint(2, None)
        return ""


class _InterruptingSession(_FakeSession):
    async def prompt_async(self, *args, **kwargs) -> str:
        raise KeyboardInterrupt


def test_sigint_graceful_shutdown_exits_active_prompt():
    """Test first Ctrl-C exits the active prompt cleanly."""
    prompt = _DummyPrompter()
    app = _FakeApp(running=True)
    prompt._session = _FakeSession(app)
    prompt._is_running = True

    prompt._handle_sigint(2, None)

    assert prompt.shutdown_requested is True
    assert prompt.is_running is False
    assert app.exit_calls == [{"result": "", "exception": None, "style": ""}]


def test_sigint_graceful_shutdown_without_active_prompt():
    """Test Ctrl-C still shuts down cleanly when no prompt app is active."""
    prompt = _DummyPrompter()
    prompt._session = _FakeSession(None)
    prompt._is_running = True

    prompt._handle_sigint(2, None)

    assert prompt.shutdown_requested is True
    assert prompt.is_running is False


def test_sigint_force_shutdown_raises_on_second_press():
    """Test second Ctrl-C forces the loop to exit immediately."""
    prompt = _DummyPrompter()
    prompt._session = _FakeSession(_FakeApp(running=False))
    prompt._is_running = True

    prompt._handle_sigint(2, None)

    with pytest.raises(SystemExit) as excinfo:
        prompt._handle_sigint(2, None)

    assert excinfo.value.code == 130
    assert prompt.outputs[-1] == "Forced shutdown requested."


def test_run_handles_prompt_keyboardinterrupt_gracefully():
    """Test prompt-side Ctrl-C exits without surfacing a traceback."""

    async def scenario() -> None:
        prompt = _DummyPrompter()
        prompt._session = _GracefulInterruptSession(prompt, _FakeApp(running=True))

        await prompt.run()

        assert prompt.shutdown_requested is True
        assert prompt.outputs[-1] == (
            "Graceful shutdown requested. Waiting for the current operation to "
            "finish. Press Ctrl-C again to force exit."
        )

    asyncio.run(scenario())


def test_run_handles_direct_prompt_keyboardinterrupt_gracefully():
    """Test a direct prompt KeyboardInterrupt still exits gracefully."""

    async def scenario() -> None:
        prompt = _DummyPrompter()
        prompt._session = _InterruptingSession(_FakeApp(running=False))

        await prompt.run()

        assert prompt.shutdown_requested is True
        assert prompt.outputs[-1] == (
            "Graceful shutdown requested. Waiting for the current operation to "
            "finish. Press Ctrl-C again to force exit."
        )

    asyncio.run(scenario())


def test_completer_supports_grouped_commands():
    """Test prompt completion for grouped command paths."""

    async def motor_start() -> None:
        return None

    prompt = _DummyPrompter()
    prompt.register_command(motor_start, alias="motor start")
    completer = prompt.completer()

    root = [
        completion.text
        for completion in completer.get_completions(Document("mo"), CompleteEvent())
    ]
    nested = [
        completion.text
        for completion in completer.get_completions(Document("motor "), CompleteEvent())
    ]

    assert root == ["motor"]
    assert nested == ["start"]
