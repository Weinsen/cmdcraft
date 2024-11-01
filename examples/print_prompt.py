#!/usr/bin/env python3
"""cmdcraft example using Prompter."""

import asyncio

from cmdcraft import Prompter


async def test_input(prompt: str) -> None:
    print(f"The input is: {prompt}")


async def main():
    prompt = Prompter()
    prompt.register_command(test_input)
    await prompt.run()


if __name__ == "__main__":
    asyncio.run(main())
