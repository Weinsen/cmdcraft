#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Callable wrapper for info extraction."""

from __future__ import annotations

from enum import Enum


class Parameter:
    """Parameter wrapper.

    This class handles individual parameters to extract information about its
    annotation type, name and default value.
    """

    def __init__(
        self, name: str, ptype: type | None = None, default: any = None
    ) -> None:
        """Construct a new Parameter object.

        Args:
            name (str): Parameter name.
            ptype (type | None, optional): Parameter type. Defaults to None.
            default (any, optional): Default value. Defaults to None.
        """
        self._name = name
        self._type = ptype
        self._default = default

    @property
    def name(self) -> str:
        """Return parameter name.

        Returns:
            str: Parameter name.
        """
        return self._name

    @property
    def default(self) -> any:
        """Return parameter default value.

        Returns:
            any: Default value.
        """
        return self._default

    @property
    def options(self) -> list[str]:
        """Return parameter options.

        Returns:
            list[str]: List of options.
        """
        if issubclass(self._type, Enum):
            return self._type._member_names_
        return []

    def cast(self, value: str) -> any:
        """Cast a value to this parameter type.

        Args:
            value (str): Value to be cast.

        Returns:
            any: The cast value.
        """
        if issubclass(self._type, Enum):
            return self._type[value]
        if self._type:
            return self._type(value)
        return value
