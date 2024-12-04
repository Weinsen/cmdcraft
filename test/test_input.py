#!/usr/bin/env python3

import pytest

from cmdcraft.input import Input, InputState


def test_tokenize():
    """Test tokenize cases."""
    assert Input.tokenize("") == []
    assert Input.tokenize("test par") == ["test", "par"]
    assert Input.tokenize("test par=2") == ["test", "par=2"]
    assert Input.tokenize('test par="1 2"') == ["test", "par=1 2"]
    with pytest.raises(Exception):
        assert Input.tokenize('test par="1') == ["test", "par=1"]


def test_position():
    """Test position method."""

    def test_input(prompt: str, position: int):
        i = Input(prompt)
        i.process()
        assert i.position == position

    test_input("", 0)
    test_input("test", 0)
    test_input("test ", 1)
    test_input("test arg", 1)
    test_input("test arg ", 2)
    test_input("test --arg=", 1)
    test_input("test --arg=v", 1)
    test_input("test --arg=v ", 2)


def test_state():
    """Test state method."""

    def test_input(prompt: str, state: InputState):
        i = Input(prompt)
        i.process()
        assert i.state == state

    test_input("", InputState.EMPTY)
    test_input("test", InputState.TYPING_PARAMETER)
    test_input("test ", InputState.TYPING_COMPLETE)
    test_input("test arg", InputState.TYPING_PARAMETER)
    test_input("test arg ", InputState.TYPING_COMPLETE)
    test_input("test --arg", InputState.TYPING_OPTION)
    test_input("test --arg=", InputState.TYPING_VALUE)
    test_input("test --arg=v", InputState.TYPING_VALUE)
    test_input("test --arg=v ", InputState.TYPING_COMPLETE)


def test_input_empty():
    """Test methods for an empty input."""
    input = Input("")
    input.process()
    assert input.tokens == []
    assert input.position == 0
    assert input.state == InputState.EMPTY


def test_input_first_argument_incomplete():
    """Test methods for an incomplete argument."""
    input = Input("test1")
    input.process()
    assert input.tokens == ["test1"]
    assert input.position == 0
    assert input.state == InputState.TYPING_PARAMETER


def test_input_first_argument_complete():
    """Test methods for a complete argument."""
    input = Input("test1 ")
    input.process()
    assert input.tokens == ["test1"]
    assert input.position == 1
    assert input.state == InputState.TYPING_COMPLETE


def test_input_second_argument_incomplete():
    """Test methods for an incomplete argument."""
    input = Input("test1 test2")
    input.process()
    assert input.tokens == ["test1", "test2"]
    assert input.position == 1
    assert input.state == InputState.TYPING_PARAMETER


def test_input_second_argument_complete():
    """Test methods for a complete argument."""
    input = Input("test1 test2 ")
    input.process()
    assert input.tokens == ["test1", "test2"]
    assert input.position == 2
    assert input.state == InputState.TYPING_COMPLETE


def test_input_option_incomplete():
    """Test methods for an incomplete option."""
    input = Input("test1 --opt")
    input.process()
    assert input.tokens == ["test1", "--opt"]
    assert input.position == 1
    assert input.state == InputState.TYPING_OPTION


def test_input_option_value():
    """Test methods for an incomplete option value."""
    input = Input("test1 --opt=v")
    input.process()
    assert input.tokens == ["test1", "--opt=v"]
    assert input.position == 1
    assert input.state == InputState.TYPING_VALUE


def test_input_option_complete():
    """Test methods for a complete option."""
    input = Input("test1 --opt=value ")
    input.process()
    assert input.tokens == ["test1", "--opt=value"]
    assert input.position == 2
    assert input.state == InputState.TYPING_COMPLETE
