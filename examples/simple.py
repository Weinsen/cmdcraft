#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CommandCraft example using Interpreter."""

import asyncio

from cmdcraft import Interpreter


async def main():
    """Example main function."""
    cli = Interpreter()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
