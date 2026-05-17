# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Callable wrapper for info extraction."""

from __future__ import annotations

from enum import Enum


class Parameter:
    """Parameter wrapper.

    This class handles individual parameters to extract information about its
    annotation type, name and default value.
    """

    def __init__(
        self, name: str, ptype: type | None = None, default: any | None = None
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
        self._dyn_opts = None

    def _supports_runtime_cast(self) -> bool:
        """Return whether the parameter annotation can be cast at runtime.

        Returns:
            bool: True if the annotation can be cast at runtime, False otherwise.

        """
        return isinstance(self._type, type)

    def _is_enum_type(self) -> bool:
        """Return whether the parameter annotation is an enum type.

        Returns:
            bool: True if the annotation is an enum type, False otherwise.

        """
        return self._supports_runtime_cast() and issubclass(self._type, Enum)

    @property
    def is_enum_type(self) -> bool:
        """Return whether the parameter annotation is an enum type.

        Returns:
            bool: True if the annotation is an enum type, False otherwise.

        """
        return self._is_enum_type()

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
        if self._dyn_opts is not None:
            return self._dyn_opts()
        elif self._is_enum_type():
            return self._type._member_names_
        return []

    def cast(self, value: str) -> any:
        """Cast a value to this parameter type.

        Args:
            value (str): Value to be cast.

        Returns:
            any: The cast value.

        """
        if self._is_enum_type():
            try:
                return self._type[value]
            except KeyError:
                options = ", ".join(self.options)
                raise ValueError(
                    f"Invalid value for parameter '{self.name}': {value!r}. "
                    f"Expected one of: {options}."
                ) from None
        if self._supports_runtime_cast():
            try:
                return self._type(value)
            except (TypeError, ValueError):
                type_name = getattr(self._type, "__name__", str(self._type))
                raise ValueError(
                    f"Invalid value for parameter '{self.name}': {value!r}. "
                    f"Expected {type_name}."
                ) from None
        return value

    def set_dynamic_options(self, generator: callable) -> None:
        """Set dynamic options for the parameter.

        This allows the completer to suggest options based on previous operations, like
        connected usernames.

        Args:
            generator (callable): Callable which should return a list of options.

        """
        self._dyn_opts = generator
