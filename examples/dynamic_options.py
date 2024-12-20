#!/usr/bin/env python3
"""cmdcraft example using Prompter."""

import asyncio
from enum import Enum

from cmdcraft import Prompter


class EnumTest(Enum):
    A = 1
    B = 2


async def test_input(a: EnumTest, *, prompt: str) -> None:
    print(f"The input is: {prompt}")


def test() -> list[str]:
    r = ("a", "b", "c")
    return r


async def main():
    prompt = Prompter()
    cmd = prompt.register_command(test_input)
    cmd.parameter("prompt").set_dynamic_options(test)
    await prompt.run()


if __name__ == "__main__":
    asyncio.run(main())
