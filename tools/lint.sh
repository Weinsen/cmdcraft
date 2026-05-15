#!/bin/bash
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

usage() {
    echo "Usage: $0 [--all|--changed]" >&2
}

scope=all

case "${1:-}" in
    "")
        ;;
    --all)
        scope=all
        ;;
    --changed)
        scope=changed
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        usage
        exit 1
        ;;
esac

PYTHON_BIN=$(tool_python_bin)
FILES=$(tool_python_targets_for_scope "$scope")

if [ -z "${FILES}" ]; then
    exit 0
fi

"${PYTHON_BIN}" -m ruff check ${FILES}
"${PYTHON_BIN}" -m ruff format --check ${FILES}