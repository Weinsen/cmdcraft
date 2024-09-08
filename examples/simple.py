#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CommandCraft example using SimpleInterpreter."""

import asyncio

from cmdcraft import SimpleInterpreter


async def main():
    """Example main function."""
    cli = SimpleInterpreter()
    await cli.init()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
