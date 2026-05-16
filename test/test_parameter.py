# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Tests for Parameter."""

from enum import Enum

import pytest

from cmdcraft.parameter import Parameter


def test_name():
    """Test the name property method."""
    par = Parameter("parameter1", str)
    assert par.name == "parameter1"


def test_default():
    """Test the default property method."""
    par = Parameter("parameter1", int)
    assert par.default is None

    par = Parameter("parameter2", str, "default value")
    assert par.default == "default value"


def test_parameter_str():
    """Test method for a `str` parameter."""
    par = Parameter("options", str, "0")
    assert par.options == []
    assert par.default == "0"
    assert par.cast("1001") == "1001"


def test_parameter_untyped():
    """Test method for an untyped parameter."""
    par = Parameter("options")
    assert par.options == []
    assert par.cast("1001") == "1001"


def test_parameter_int():
    """Test method for a `int` parameter."""
    par = Parameter("options", int, 0)
    assert par.options == []
    assert par.default == 0
    assert par.cast("1001") == 1001

    with pytest.raises(Exception):
        assert par.cast("ARG")


def test_parameter_enum():
    """Test method for a `Enum` parameter."""

    class TestEnum(Enum):
        OPT_0 = 0
        OPT_A = 1
        OPT_B = 2

    par = Parameter("options", TestEnum, TestEnum.OPT_0)
    assert par.options == ["OPT_0", "OPT_A", "OPT_B"]
    assert par.default == TestEnum.OPT_0
    assert par.cast("OPT_A") == TestEnum.OPT_A

    with pytest.raises(ValueError) as excinfo:
        par.cast("OPT_Z")

    assert (
        str(excinfo.value)
        == "Invalid value for parameter 'options': 'OPT_Z'. "
        "Expected one of: OPT_0, OPT_A, OPT_B."
    )
