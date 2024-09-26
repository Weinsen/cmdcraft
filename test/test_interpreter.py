#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from cmdcraft.base import BasePrompter as BI

def test_tokenize():
    assert BI.tokenize("") == []
    assert BI.tokenize("test par") == ["test", "par"]
    assert BI.tokenize("test par=2") == ["test", "par=2"]
    assert BI.tokenize("test par=\"1 2\"") == ["test", "par=1 2"]
    assert BI.tokenize("test par=\"1") == ["test", "par=1"]
