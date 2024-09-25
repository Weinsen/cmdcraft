#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cmdcraft example using Interpreter."""

import asyncio

from cmdcraft import Interpreter


async def test_input(prompt: str) -> None:
    print(f"The input is: {prompt}")


async def main():
    prompt = Interpreter()
    prompt.register_command(test_input)
    await prompt.run()


if __name__ == "__main__":
    asyncio.run(main())
