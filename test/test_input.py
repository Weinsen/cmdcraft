#!/usr/bin/env python3

import pytest

from cmdcraft.input import Input as I


def test_tokenize():
    assert I.tokenize("") == []
    assert I.tokenize("test par") == ["test", "par"]
    assert I.tokenize("test par=2") == ["test", "par=2"]
    assert I.tokenize('test par="1 2"') == ["test", "par=1 2"]
    with pytest.raises(Exception):
        assert I.tokenize('test par="1') == ["test", "par=1"]
