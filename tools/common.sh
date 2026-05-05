#!/usr/bin/env bash
#
# Shared functions for OARepo runner scripts (library_runner.sh and repository_runner.sh).
#
# This file is sourced by both runners and should not be executed directly.
# When deployed to a project, it is cached as .runner-common.sh alongside .runner.sh.
#
# (C) 2025 CESNET, z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#

# region: Colored echo functions
echo_progress() {
    echo -e "\033[0;37m→ $*\033[0m" >&2
}

echo_success() {
    echo >&2
    echo -e "\033[0;32m✓ $*\033[0m" >&2
}

echo_warning() {
    echo >&2
    echo -e "\033[0;33m⚠ $*\033[0m" >&2
}

echo_error() {
    echo >&2
    echo -e "\033[0;31m✗ $*\033[0m" >&2
}

echo_user() {
    echo >&2
    echo -e "\033[0;36m➜ $*\033[0m" >&2
}
# endregion: Colored echo functions

# region: Package info helpers
get_package_name() {
    local name
    name=$(
        egrep '^name' "pyproject.toml" |
        head -n 1 |
        sed 's/[^"]*"//' |
        sed 's/".*//'
    )

    if [ -z "$name" ]; then
        echo_error "No package name found in pyproject.toml, please add one."
        exit 1
    else
        echo "$name"
    fi
}

get_home_page() {
    local hp
    hp=$(
        egrep '^Homepage' "pyproject.toml" |
        head -n 1 |
        sed 's/[^"]*"//' |
        sed 's/".*//'
    )
    if [ -z "$hp" ]; then
        echo_error "No homepage found in pyproject.toml, please add one."
        exit 1
    else
        echo "$hp"
    fi
}
# endregion: Package info helpers

# region: Code directory detection
detect_code_directories() {
    # Detects source code directories for linting/testing.
    # Pass "false" as first arg to exclude the tests directory.
    # Sets the global code_directories array.
    local include_tests="${1:-true}"
    local pkg_name
    pkg_name=$(get_package_name)

    code_directories=()

    if [ -d "src" ]; then
        code_directories+=("src")
    else
        local top_level
        top_level=$(echo "${pkg_name}" | tr '-' '_')
        if [ -d "${top_level}" ]; then
            code_directories+=("${top_level}")
        else
            # check [tool.uv.build-backend] module-name = ["common", "ui", ...]
            if grep -q '^\[tool.uv.build-backend\]' pyproject.toml; then
                local modules
                modules=$(
                    sed -n '/^\[tool.uv.build-backend\]/,/^\[/p' pyproject.toml |
                    sed '/^\[/d' |
                    tr '\n' ' ' |
                    sed 's/.*module-name *= *//' |
                    sed 's/\].*//' |
                    tr ',' '\n' |
                    tr -d '[]"' |
                    sed 's/^ *//;s/ *$//' |
                    grep -v '^$'
                )
                while IFS= read -r mod; do
                    if [ -n "$mod" ] && [ -d "$mod" ]; then
                        code_directories+=("$mod")
                    fi
                done <<< "$modules"
            # check [tool.hatch.build.targets.wheel] packages = ["oarepo_oaipmh_harvester"]
            elif grep -q '^\[tool.hatch.build.targets.wheel\]' pyproject.toml; then
                top_level=$(
                    cat pyproject.toml |
                    tr '\n' '$$$' |
                    sed 's/.*\[tool.hatch.build.targets.wheel\]//' |
                    tr '$$$' '\n' |
                    grep '^packages' |
                    sed 's/packages *= *\[ *"//' | sed 's/".*//'
                )
                code_directories+=("${top_level}")
            else
                echo_error "No src/ or ${top_level}/ directory found, please ensure your package structure is correct."
                exit 1
            fi
        fi
    fi

    if [ "$include_tests" = "true" ] && [ -d "tests" ]; then
        code_directories+=("tests")
    fi

    export code_directories
}
# endregion: Code directory detection

# region: Invenio CLI wrapper
run_invenio_cli() {
    set -euo pipefail

    # temporary implementation until release
    uvx ${PYTHON:+--python="$PYTHON"} \
        --with git+https://github.com/oarepo/oarepo-cli@rdm-14 \
        --from git+https://github.com/oarepo/invenio-cli@oarepo-feature-docker-environment \
        invenio-cli "$@"
}
# endregion: Invenio CLI wrapper

# region: Self-update helper
self_update_common() {
    # Downloads the latest common.sh alongside the runner.
    # Called from each runner's self_update function.
    local common_path
    common_path="$(dirname "${BASH_SOURCE[1]}")/.runner-common.sh"

    echo_progress "Updating common runner functions..."
    curl --fail -o "${common_path}.new" \
        https://raw.githubusercontent.com/oarepo/oarepo/main/tools/common.sh
    chmod +x "${common_path}.new"
    mv "${common_path}.new" "$common_path"
}
# endregion: Self-update helper

# region: Linting and formatting

run_linters() {
    set -e
    set -o pipefail

    if [ ${#code_directories[@]} -eq 0 ]; then
        echo_error "code_directories is not set. Call detect_code_directories first."
        return 1
    fi

    cat <<EOF >.ruff.toml
target-version = "py313"
line-length = 120
indent-width = 4

[lint]
select = [ "ALL" ]
ignore = [
    "FIX002",  # exclude TODO comments
    "TD003",   # Missing issue link for this TODO
    "TD002",   # Missing author in TODO
    "N806",    # Variable name should be lowercase as we dynamically create classes
    "ANN204",  # Missing return type annotation for __init__
    "ANN401",  # Any in *args/**kwargs
    "TRY003",  # Avoid long exception messages
    "EM101",   # Avoid using string literal in exception
    "EM102",   # Avoid using f-string literal in exception
    "TRY301",  # Avoid raising/catching the same exception type
    "PLC0415",  # Place imports to the top of the file
    "PGH004",  # Use specific noqa for pylint
    "TID252",  # Prefer absolute imports
    "D203",    # Using D211
    "D213",    # Using D212 (multi-line-summary-first-line) instead
    "COM812",
    "FBT001",  # Avoid using boolean function parameters
    "FBT002",  # Avoid using boolean function parameters
]

[lint.per-file-ignores]
"__init__.py" = ["E402"]
"**/{tests,docs,tools}/*" = [
    "E402",
    "S101",
    "ANN001",
    "ARG001",
    "D103",
    "ANN201",
    "D100",
    "INP",
    "PLR",
    "PLC"
    ]

[format]
docstring-code-format = true
docstring-code-line-length = 40
EOF

    uvx -p python3.14 ruff check --exclude pyproject.toml
    uvx -p python3.14 ruff format --check --exclude pyproject.toml
    check_license_headers
    check_future_annotations

    cat <<EOF >.mypy.ini
[mypy]
warn_return_any = True
warn_unused_configs = True
warn_unreachable = True
follow_untyped_imports = True
EOF

    local venv_python="${UV_PROJECT_ENVIRONMENT:-.venv}/bin/python"
    uvx --with types-PyYAML --with types-requests -p "$venv_python" mypy "${code_directories[0]}" --ignore-missing-imports --exclude os-v2
    uvx pyright --pythonpath "$venv_python" "${code_directories[0]}"
}

format_code() {
    set -e
    set -o pipefail

    uvx ruff format --exclude pyproject.toml
    uvx ruff check --fix --exclude pyproject.toml
}

check_license_headers() {
    set -e
    set -o pipefail

    if [ -f .check_ok.txt ]; then rm .check_ok.txt; fi
    if [ -f .check_errors.txt ]; then rm .check_errors.txt; fi
    touch .check_ok.txt
    touch .check_errors.txt

    # Check for license headers in Python files
    find "${code_directories[@]}" -name "*.py" | while read -r file; do
        if grep -iq "Copyright (c)" "$file"; then
            echo "$file" >>.check_ok.txt
        else
            echo "Missing license header in $file"
            grep -i "Copyright (c)" "$file" || true
            echo "$file" >>.check_errors.txt
        fi
    done

    local errors
    errors=$(wc -l < .check_errors.txt)
    rm .check_ok.txt .check_errors.txt

    if [ "$errors" -gt 0 ]; then
        echo "${errors} file(s) are missing license headers." >&2
        return 1
    fi
}

check_future_annotations() {
    set -e
    set -o pipefail

    if [ -f .check_ok.txt ]; then rm .check_ok.txt; fi
    if [ -f .check_errors.txt ]; then rm .check_errors.txt; fi
    touch .check_ok.txt
    touch .check_errors.txt

    # Check for future annotations in Python files
    find "${code_directories[@]}" -name "*.py" -not -path "./.venv/*" | while read -r file; do
        if grep "from __future__" "$file" | grep -q "annotations"; then
            echo "$file" >>.check_ok.txt
        else
            echo "Missing 'from __future__ import annotations' in $file" >&2
            echo "$file" >>.check_errors.txt
        fi
    done

    local errors
    errors=$(wc -l < .check_errors.txt)
    rm .check_ok.txt .check_errors.txt

    if [ "$errors" -gt 0 ]; then
        echo "${errors} file(s) are missing future annotations." >&2
        return 1
    fi
}

add_license_headers() {
    set -e
    set -o pipefail

    local current_year home_page pkg_name
    current_year=$(date +%Y)
    ORGANIZATION=${ORGANIZATION:-"CESNET z.s.p.o"}
    home_page=$(get_home_page)
    pkg_name=$(get_package_name)

    cat <<'EOF' > /tmp/license-header.txt
Copyright (c) ${years} ${owner}.

This file is a part of ${projectname} (see ${projecturl}).

${projectname} is free software; you can redistribute it and/or modify it
under the terms of the MIT License; see LICENSE file for more details.
EOF

    find "${code_directories[@]}" -name "*.py" -not -path "./.venv/*" | while read -r file; do
        if ! grep -iq "Copyright (C)" "$file"; then
            uvx licenseheaders -t /tmp/license-header.txt -y "$current_year" \
                -o "$ORGANIZATION" -n "$pkg_name" \
                -u "$home_page" -f "$file"
        fi
    done
}

run_jslint() {
    set -e
    set -o pipefail

    if [ ! -f package.json ]; then
        echo "No package.json found, skipping JavaScript linting."
        return 0
    fi

    if ! jq -e '.devDependencies."@inveniosoftware/eslint-config-invenio"' package.json > /dev/null; then
        echo "Adding @inveniosoftware/eslint-config-invenio to dev dependencies..."
        pnpm add -D @inveniosoftware/eslint-config-invenio@2
    fi

    if [ ! -x node_modules/.bin/eslint ] ; then
        echo "Installing ESLint..."
        pnpm install
    fi

    echo "Copying ESLint configuration files..."
    # create eslint config file
    cat <<'EOF' >.eslintrc.yaml
extends:
- '@inveniosoftware/eslint-config-invenio'
- '@inveniosoftware/eslint-config-invenio/prettier'

rules:
  react/require-default-props: 'off'

settings:
  react:
    version: "16"

parser: '@babel/eslint-parser'
EOF

    # run eslint
    echo "Running ESLint..."
    node_modules/.bin/eslint --ext .js,.jsx --fix --no-error-on-unmatched-pattern "${code_directories[@]}"

    # run prettier. Locally do --write and in CI just --check
    echo "Running Prettier..."
    if [ "${CI:-false}" = "true" ]; then
        prettier_flag="--check"
    else
        prettier_flag="--write"
    fi

    # Run prettier on only .js/.jsx files within the specified directories
    local prettier_globs=()
    for dir in "${code_directories[@]}"; do
        prettier_globs+=("${dir}/**/*.js" "${dir}/**/*.jsx")
    done
    node_modules/.bin/prettier "$prettier_flag" --no-error-on-unmatched-pattern "${prettier_globs[@]}"

    return 0
}

# endregion: Linting and formatting

# region: Test services (isolated containers for testing)
start_test_services() {
    set -euo pipefail

    echo_progress "Starting isolated test services..."
    uvx --with setuptools docker-services-cli up \
        --db "${DB:-postgresql}" --search "${SEARCH:-opensearch}" \
        --mq "${MQ:-rabbitmq}" --cache "${CACHE:-redis}" --s3 "${S3:-minio}" --env \
    > .env-services

    source .env-services
}

stop_test_services() {
    set -euo pipefail

    echo_progress "Stopping test services..."
    eval "$(uvx --with setuptools docker-services-cli down --env)"
    if [ -f .env-services ]; then
        rm .env-services
    fi
}
# endregion: Test services

# region: Test runner
setup_test_coverage() {
    # Sets up coverage reporting. Expects code_directories to be set.
    uv pip install pytest-cov
    export PYTEST_ADDOPTS="--cov=${code_directories[0]} --cov-branch --cov-report=json --cov-report=html --cov-report=xml --cov-report=term-missing:skip-covered --junitxml=junit.xml -o junit_family=legacy"
    echo_progress "Running tests with coverage enabled"
}
# endregion: Test runner
