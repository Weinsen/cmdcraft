#!/bin/sh
# *****************************************************************************
# Copyright (c) 2024-2026, Antonio Mario Weinsen Junior
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# *****************************************************************************

tool_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null || pwd
}

tool_first_existing_ref() {
    for ref in "$@"; do
        if [ -n "$ref" ] && git rev-parse --verify --quiet "${ref}^{commit}" >/dev/null; then
            printf '%s\n' "$ref"
            return 0
        fi
    done

    return 1
}

tool_python_bin() {
    if [ -n "${PYTHON:-}" ]; then
        printf '%s\n' "${PYTHON}"
        return 0
    fi

    if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
        printf '%s\n' "${VIRTUAL_ENV}/bin/python"
        return 0
    fi

    repo_root=$(tool_repo_root)
    if [ -x "${repo_root}/.venv/bin/python" ]; then
        printf '%s\n' "${repo_root}/.venv/bin/python"
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        printf '%s\n' 'python3'
        return 0
    fi

    if command -v python >/dev/null 2>&1; then
        printf '%s\n' 'python'
        return 0
    fi

    echo 'No Python interpreter found on PATH.' >&2
    return 1
}

tool_resolve_base_ref() {
    base_ref_override=${TOOLS_BASE_REF:-${CMDCRAFT_BASE_REF:-}}
    if [ -n "${base_ref_override}" ]; then
        tool_first_existing_ref "${base_ref_override}" "origin/${base_ref_override}"
        return $?
    fi

    if [ -n "${GITHUB_BASE_REF:-}" ]; then
        tool_first_existing_ref "origin/${GITHUB_BASE_REF}" "${GITHUB_BASE_REF}"
        return $?
    fi

    if [ -n "${GITHUB_SHA:-}" ] && git rev-parse --verify --quiet HEAD^ >/dev/null; then
        printf '%s\n' 'HEAD^'
        return 0
    fi

    if git symbolic-ref refs/remotes/origin/HEAD >/dev/null 2>&1; then
        git symbolic-ref --short refs/remotes/origin/HEAD
        return 0
    fi

    tool_first_existing_ref origin/master master origin/main main
}

tool_tracked_python_files() {
    git ls-files '*.py'
}

tool_changed_python_files() {
    all_files=${TOOLS_ALL_FILES:-${CMDCRAFT_ALL_FILES:-0}}
    if [ "${all_files}" = "1" ]; then
        tool_tracked_python_files
        return 0
    fi

    base_ref=$(tool_resolve_base_ref 2>/dev/null || true)
    if [ -n "$base_ref" ]; then
        git diff --name-only --diff-filter=d "$base_ref" -- '*.py'
        return 0
    fi

    tool_tracked_python_files
}

tool_python_targets() {
    tool_changed_python_files | sed '/^$/d'
}

tool_python_targets_for_scope() {
    case "${1:-changed}" in
        changed)
            tool_changed_python_files
            ;;
        all)
            tool_tracked_python_files
            ;;
        *)
            echo "Unknown scope: ${1}" >&2
            return 1
            ;;
    esac | sed '/^$/d'
}