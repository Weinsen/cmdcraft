#!/bin/sh
# *****************************************************************************
# Copyright (c) 2024, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

# Test only new / modified files
# FILES=$(git diff --name-only --diff-filter=d develop | grep -E "(\.py$)")
FILES=$(find . -name *.py)
echo $FILES

if [ -z "${FILES}" ]; then
    exit 0
fi

isort ${FILES}
black ${FILES}