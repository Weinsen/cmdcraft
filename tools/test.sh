#!/bin/sh
# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SCRIPT_DIR/common.sh"

PYTHON_BIN=$(tool_python_bin)

"${PYTHON_BIN}" -m pytest test "$@"