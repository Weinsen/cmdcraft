#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Callable wrapper for info extraction."""

from __future__ import annotations

import asyncio
import inspect
from typing import get_type_hints

from .parameter import Parameter


class Command:
    """Command wrapper.

    This class handles commands / callables to extract information, specially its
    parameters.
    """

    def __init__(self, cb: callable, alias: str | None = None) -> None:
        """Construct a Command object.

        Args:
            cb (callable): Callable to be wrapped.
            alias (str | None, optional): Command name. Defaults to None.
        """
        self._cb: callable = cb
        self._pars: dict[str, Parameter] = {}
        self._positional: dict[str, Parameter] = {}
        self._name: str = cb.__name__
        self._alias: str = alias if alias is not None else self.name

    @property
    def __doc__(self) -> str:
        """Return the original callable docstring.

        Returns:
            str: Command docstring.
        """
        d = self._cb.__doc__
        fb = ""
        return d if d is not None else fb

    @property
    def name(self) -> str:
        """Return the command name.

        Returns:
            str: Command name.
        """
        return self._name

    @property
    def alias(self) -> str:
        """Return the command alias.

        Returns:
            str: Command alias.
        """
        return self._alias

    @property
    def parameters(self) -> dict[str, Parameter]:
        """Return a dictionary of parameters.

        Returns:
            dict[str, Parameter]: Parameters.
        """
        return self._pars

    def list_parameters(self) -> list[str]:
        """Return a list of parameters.

        Returns:
            list[str]: List of parameters.
        """
        return list(self._pars)

    def eval(self, *args) -> asyncio.Future:
        """Evaluate a call.

        Returns:
            asyncio.Future: A future of this callable.
        """
        pos: list[str] = [x for x in args if "=" not in x]
        kws: list[str] = [x for x in args if "=" in x]

        args = []
        for a, p in zip(pos, self._positional.values()):
            args.append(p.cast(a))

        kwargs = {}
        for kw in kws:
            [par, value] = kw.split("=")
            if par in self._pars:
                kwargs[par] = self._pars[par].cast(value)

        return self._cb(*args, **kwargs)

    def process(self) -> None:
        """Process the callable metadata."""
        f = self._cb
        anns = get_type_hints(f)
        pars = inspect.signature(f).parameters
        for k, v in pars.items():
            default = None
            ptype = None
            if v.default is not inspect.Parameter.empty:
                default = v.default
            if k in anns:
                ptype = anns[k]
            par = Parameter(k, ptype, default)

            if v.kind in (v.POSITIONAL_ONLY, v.POSITIONAL_OR_KEYWORD):
                self._positional[k] = par
            self._pars[k] = par
