#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cmdcraft example using Prompter."""

import asyncio

from cmdcraft import Prompter
from enum import Enum

class EnumTest(Enum):
    A = 1
    B = 2


async def test_input(s: str, a: EnumTest, /, prompt: str) -> None:
    print(f"The input is: {prompt}")

def test() -> list[str]:
    r = ("a", "b", "c")
    return r


async def main():
    prompt = Prompter()
    cmd = prompt.register_command(test_input)
    cmd.parameter("prompt").set_dynamic_options(test)
    cmd.parameter("s").set_dynamic_options(test)
    await prompt.run()


if __name__ == "__main__":
    asyncio.run(main())
