#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CommandCraft example using PromptInterpreter."""

import asyncio

from cmdcraft import PromptInterpreter


async def main():
    """Example main function."""
    cli = PromptInterpreter()
    await cli.init()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
