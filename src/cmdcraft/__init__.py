#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CommandCraft module."""

from __future__ import annotations

from .base import BaseInterpreter
from .prompt import PromptInterpreter
from .simple import SimpleInterpreter

__version__ = "0.0.1"

__all__ = [
    "SimpleInterpreter",
    "BaseInterpreter",
    "PromptInterpreter",
    "__version__",
]
