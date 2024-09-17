#!/bin/sh
# *****************************************************************************
# Copyright (c) 2024, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

rm -rf docs/build
sphinx-build -M html docs/source docs/build