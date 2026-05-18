# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************
"""cmdcraft example using grouped commands."""

import asyncio

from cmdcraft import Prompter


async def start() -> None:
    """Start the motor."""
    print("motor started")


async def stop() -> None:
    """Stop the motor."""
    print("motor stopped")


async def home() -> None:
    """Home the motor axis."""
    print("motor axis homed")


async def move(position: float) -> None:
    """Move the motor axis to a position.

    Args:
        position (float): Target axis position.

    Returns:
        None: This coroutine does not return a value.

    """
    print(f"moving motor axis to {position}")


async def main() -> None:
    """Run the grouped command example.

    Returns:
        None: This coroutine does not return a value.

    """
    prompt = Prompter()

    motor = prompt.register_group("motor", doc="Motor related commands.")
    motor.register_command(start)
    motor.register_command(stop)

    axis = prompt.register_group("motor axis", doc="Motor axis commands.")
    axis.register_command(home)
    prompt.register_command(move, alias="motor axis move")

    await prompt.run()


if __name__ == "__main__":
    asyncio.run(main())
