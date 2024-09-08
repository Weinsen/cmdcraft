#!/usr/bin/env python
# *****************************************************************************
# Copyright (c) 2024, Antonio Mario Weinsen Junior <weinsen.mbed@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

from cmdcraft import SimpleInterpreter

import asyncio

async def main():

    cli = SimpleInterpreter()
    await cli.connect()
    await cli.run()

if __name__ == '__main__':
    asyncio.run(main())

