# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""Command grouping utilities."""

from __future__ import annotations

from collections.abc import Callable

from .command import Command


def split_command_path(path: str) -> list[str]:
    """Split a command path into its segments.

    Args:
        path (str): Command path separated by spaces.

    Returns:
        list[str]: Non-empty path segments.

    Raises:
        ValueError: If the provided path is empty.

    """
    parts = path.split()
    if not parts:
        raise ValueError("Command paths cannot be empty.")
    return parts


def _leaf_group_name(name: str, alias: str | None) -> str:
    """Return the group name that should be used at the leaf node.

    Args:
        name (str): Requested group name.
        alias (str | None): Requested group alias.

    Returns:
        str: Leaf group name.

    """
    if alias is None:
        return split_command_path(name)[-1]
    return name


def _raise_name_conflict(path: str) -> None:
    """Raise a standardized registration conflict error.

    Args:
        path (str): Conflicting path.

    Returns:
        None: This helper does not return a value.

    Raises:
        ValueError: Always raised for conflicting registrations.

    """
    raise ValueError(f"A command or group is already registered at '{path}'.")


class CommandGroup:
    """Namespace for commands and nested groups."""

    def __init__(
        self,
        name: str,
        alias: str | None = None,
        doc: str | None = None,
    ) -> None:
        """Build a command group.

        Args:
            name (str): Group name.
            alias (str | None, optional): Group alias. Defaults to None.
            doc (str | None, optional): Group documentation. Defaults to None.

        Returns:
            None: This constructor does not return a value.

        """
        self._name = name
        self._alias = alias if alias is not None else name
        self._doc = doc
        self._commands: dict[str, Command | CommandGroup] = {}

    @property
    def name(self) -> str:
        """Return the group name.

        Returns:
            str: The registered group name.

        """
        return self._name

    @property
    def alias(self) -> str:
        """Return the group alias.

        Returns:
            str: The alias used in the prompt.

        """
        return self._alias

    @property
    def __doc__(self) -> str:
        """Return the group documentation.

        Returns:
            str: Group documentation text.

        """
        return self._doc or ""

    @property
    def commands(self) -> dict[str, Command | CommandGroup]:
        """Return child commands and groups.

        Returns:
            dict[str, Command | CommandGroup]: Registered child nodes.

        """
        return self._commands

    def register_group(
        self,
        name: str,
        alias: str | None = None,
        doc: str | None = None,
    ) -> CommandGroup:
        """Register a child group and return it.

        Args:
            name (str): Group name.
            alias (str | None, optional): Group alias or path. Defaults to None.
            doc (str | None, optional): Group documentation. Defaults to None.

        Returns:
            CommandGroup: The registered or reused child group.

        Raises:
            ValueError: If the group path conflicts with an existing command.

        """
        path = split_command_path(alias if alias is not None else name)
        if len(path) == 1:
            current = self._commands.get(path[0])
            if isinstance(current, CommandGroup):
                if doc is not None:
                    current._doc = doc
                return current
            if isinstance(current, Command):
                _raise_name_conflict(path[0])

            group = CommandGroup(
                _leaf_group_name(name, alias),
                alias=path[0],
                doc=doc,
            )
            self._commands[group.alias] = group
            return group

        parent = self.register_group(path[0])
        return parent.register_group(
            _leaf_group_name(name, alias),
            alias=" ".join(path[1:]),
            doc=doc,
        )

    def register_command(
        self,
        command: Callable[..., object],
        alias: str | None = None,
    ) -> Command:
        """Register a command into this group.

        Args:
            command (Callable[..., object]): Command callback.
            alias (str | None, optional): Command alias or path. Defaults to None.

        Returns:
            Command: The registered command wrapper.

        Raises:
            ValueError: If the command path conflicts with an existing command
                or group.

        """
        path = split_command_path(alias if alias is not None else command.__name__)
        if len(path) == 1:
            current = self._commands.get(path[0])
            if current is not None:
                _raise_name_conflict(path[0])

            cmd = Command(command, path[0])
            self._commands[cmd.alias] = cmd
            cmd.process()
            return cmd

        group = self.register_group(path[0])
        return group.register_command(command, alias=" ".join(path[1:]))

    def resolve(
        self,
        tokens: list[str],
    ) -> tuple[Command | CommandGroup | None, int]:
        """Resolve a token list against this group tree.

        Args:
            tokens (list[str]): Tokenized prompt input.

        Returns:
            tuple[Command | CommandGroup | None, int]: The resolved node and the
                number of consumed tokens.

        """
        current: CommandGroup = self
        node: Command | CommandGroup | None = None
        consumed = 0

        for token in tokens:
            node = current.commands.get(token)
            if node is None:
                break

            consumed += 1
            if isinstance(node, CommandGroup):
                current = node
                continue

            return node, consumed

        return node, consumed

    def command_paths(
        self,
        prefix: tuple[str, ...] = (),
        include_groups: bool = False,
    ) -> list[str]:
        """Return registered command paths.

        Args:
            prefix (tuple[str, ...], optional): Current prefix path. Defaults to ().
            include_groups (bool, optional): Include group paths in the result.
                Defaults to False.

        Returns:
            list[str]: Registered command paths.

        """
        paths: list[str] = []
        for name, node in self._commands.items():
            current = (*prefix, name)
            if isinstance(node, CommandGroup):
                if include_groups:
                    paths.append(" ".join(current))
                paths.extend(node.command_paths(current, include_groups=include_groups))
                continue

            paths.append(" ".join(current))

        return paths
