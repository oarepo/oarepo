#!/usr/bin/env bash
#
# This script sets up a Python virtual environment, installs necessary packages,
# runs tests and other tasks for libraries which are part of the OARepo Invenio RDM
# flavour.
# 
# Usage: ./run --help
#
# Note: To ensure consistency, this script is never committed to the library.
# Only the stub (library/run.sh) should be placed in the library directory.
# The actual script is downloaded from the OARepo repository on the first run and cached.
# as .runner.sh. If you want to update the script, run ./run.sh self-update.
#
# (C) 2025 CESNET, z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#

export UV_EXTRA_INDEX_URL=${UV_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export LC_TIME=${LC_TIME:-"en_US.UTF-8"}

cd "$(dirname "$0")"

if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found, please migrate from setup.cfg."
    echo "See https://github.com/oarepo/oarepo/blob/main/README.md for details."
    exit 1
fi

if [ -f setup.cfg ]; then
    echo "setup.cfg found, please migrate to pyproject.toml."
    echo "See https://github.com/oarepo/oarepo/blob/main/README.md for details."
    exit 1
fi

get_package_name() {
    name=$(
        cat "pyproject.toml" | 
        egrep '^name' | 
        head -n 1 | 
        sed 's/[^"]*"//' | 
        sed 's/".*//'
    )

    if [ -z "$name" ]; then
        echo "No package name found in pyproject.toml, please add one."
        exit 1
    else
        echo "$name"
    fi
}

get_home_page() {
    hp=$(
        cat "pyproject.toml" | 
        egrep '^Homepage' | 
        head -n 1 | 
        sed 's/[^"]*"//' | 
        sed 's/".*//'
    )
    if [ -z "$hp" ]; then
        echo "No homepage found in pyproject.toml, please add one."
        exit 1
    else
        echo "$hp"
    fi
}

package_name=$(get_package_name)
code_directories=()

if [ -d "src" ]; then
    code_directories+=("src")
else
    code_directories+=($(echo ${package_name} | tr '-' '_'))
fi

if [ -d "tests" ]; then
    code_directories+=("tests")
fi

export package_name
export code_directories


run_tools() {
    set -e
    set -o pipefail    
    
    # Parse the commandline according to the options defined above.
    export OAREPO_VERSION=${OAREPO_VERSION:-"13"}
    export PYTHON_VERSION=${PYTHON_VERSION:-"3.13"}
    export PYTHON=${PYTHON:-"python${PYTHON_VERSION}"}
    export NO_EDITABLE=${NO_EDITABLE:-0}

    while [[ $# -gt 0 ]]; do
        case $1 in
            venv)
                shift
                setup_venv --force "$@"
                return 0
                ;;
            start)
                start_services
                return 0
                ;;
            stop)
                stop_services
                return 0
                ;;
            test)
                shift
                run_tests "$@"
                return 0
                ;;
            oarepo-versions)
                list_oarepo_versions
                return 0
                ;;
            clean)
                cleanup
                return 0
                ;;
            shell)
                shift
                run_command bash "$@"
                return 0
                ;;
            invenio)
                shift
                run_command invenio "$@"
                return 0
                ;;
            translations)
                shift
                uvx --from oarepo-tools make-translations
                return 0
                ;;
            lint)
                shift
                run_linters "$@"
                return 0
                ;;
            format)
                shift
                format_code "$@"
                return 0
                ;;
            license-headers)
                shift
                add_license_headers "$@"
                return 0
                ;;
            jslint)
                shift
                run_jslint "$@"
                return 0
                ;;
            -h|--help)
                show_help
                return 0
                ;;
            self-update)
                self_update
                return 0
                ;;
            --no-editable)
                NO_EDITABLE=1
                shift
                ;;
            check-script-working)
                # This is used to check if the script is working after self-update.
                # It should return 0 if the script is working, 1 otherwise.
                echo "Script is working."
                return 0
                ;;
            *)
                echo "Unknown command: $1"
                show_help
                exit 1
                ;;
        esac
    done
    show_help
    return 0
}

show_help() {
    echo "Usage: $0 [options] [command]"
    echo ""
    echo "Commands:"
    echo "  venv              Set up the virtual environment"
    echo "      --no-editable     Do not install the package in editable mode, build it first"
    echo "      --force           Force the creation of the virtual environment, removing any existing one"
    echo "  start             Start the services for testing"
    echo "  stop              Stop the services after testing"
    echo "  test              Run the tests"
    echo "      --skip-services   Skip starting/stopping services"
    echo "      --with-coverage   Run tests with coverage enabled"
    echo "  oarepo-versions   List the supported OARepo versions for this package"
    echo "  clean             Clean up the environment (stop services, remove venv, etc.)"
    echo "  shell             Start a shell with the virtual environment and services running"
    echo "      --skip-services   Skip starting/stopping services"
    echo "  invenio           Run an Invenio command with the virtual environment and services running"
    echo "      --skip-services   Skip starting/stopping services"
    echo "  translations      Extract/compile translations for this package"
    echo "  lint              Run linters on the codebase"
    echo "  format            Format the codebase using ruff"
    echo "  license-headers   Add license headers in the codebase"
    echo "  jslint            Run JavaScript linters (ESLint and Prettier)"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  OAREPO_VERSION    The version of OARepo to use (default: 13)"
    echo "  PYTHON_VERSION    The Python interpreter to use (default: 3.13)"
    echo "  PYTHON            The Python executable to use (default: python3.13)"
    echo ""
    echo "Housekeeping commands:"
    echo "  self-update       Update the runner script"
    return 0
}   

stop_services() {
    if [ ! -z "$SKIP_SERVICES" ]; then
        return 0
    fi
    set -e
    set -o pipefail    

    eval "$(uvx --with setuptools docker-services-cli down --env)"
    if [ -f .env-services ]; then
        rm .env-services
    fi
}

start_services() {
    if [ ! -z "$SKIP_SERVICES" ]; then
        return 0
    fi
    set -e
    set -o pipefail    

    uvx --with setuptools docker-services-cli up \
        --db ${DB:-postgresql} --search ${SEARCH:-opensearch} \
        --mq ${MQ:-rabbitmq} --cache ${CACHE:-redis} --env \
    > .env-services

    source .env-services
}

list_oarepo_versions() {
    # if there is a pyproject.toml, get its dependencies section and parse the
    # "oarepo[rdm,tests]>=13.0.0,<15.0.0" line to get the version of oarepo.
    # return 13,14 in this case
    if [ -f pyproject.toml ]; then
        oarepo_version_string=$(grep 'oarepo\[rdm,tests\]' pyproject.toml | head -n 1)
        echo -n "{"
        echo -n "\"oarepo_versions\": "
        get_versions "$oarepo_version_string"
        echo -n ", "
        echo -n "\"python_versions\": "
        python_version_string=$(grep 'requires-python' pyproject.toml | head -n 1)
        get_python_versions $(get_versions "$oarepo_version_string")
        echo -n ", "
        echo -n "\"node_versions\": [\"24\"]"
        echo "}"
    else
        echo "No pyproject.toml found and other types are not supported yet."
        echo "Please ensure you are in the correct directory."
        exit 1
    fi
}

get_versions() {
    version_string=$(echo "$1" | sed 's/.*>=//' | sed 's/".*//')
    lower_bound=$(echo "$version_string" | cut -d',' -f1 | cut -d'.' -f1)
    upper_bound=$(echo "$version_string" | cut -d',' -f2 | cut -d'.' -f1 | sed 's/<//')
    if [ -z "$upper_bound" ]; then
        upper_bound=$((lower_bound + 1))
    fi
    upper_bound=$((upper_bound - 1))
    versions=$(seq "$lower_bound" "$upper_bound")
    versions=$(echo "$versions" | sed 's/^/"/' | sed 's/$/"/' | tr '\n' ',' | sed 's/,$//')
    echo -n "[$versions]"
}

get_python_versions() {
    oarepo_versions="$1"
    python_versions=()

    # if there is "12" inside oarepo_versions, return 3.12
    if [[ "$oarepo_versions" == *"12"* ]]; then
        python_versions+=("\"3.12\"")
    fi
    # for oarepo 13, return 3.13
    if [[ "$oarepo_versions" == *"13"* ]]; then
        python_versions+=("\"3.13\"")
    fi

    # return concatenated string of python versions as json array of strings
    echo -n "[$python_versions]"
}

run_command() {
    set -e
    set -o pipefail    

    command_name="$1"
    shift

    non_processed_args=()

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-services)
                SKIP_SERVICES=1
                shift
                ;;
            *)
                non_processed_args+=("$1")
                shift
                ;;
        esac
    done

    setup_venv
    if [ -z "$SKIP_SERVICES" ]; then
        start_services
    fi

    source .venv/bin/activate
    source .env-services
    "$command_name" "${non_processed_args[@]}"
}

setup_venv() {
    set -e
    set -o pipefail    

    while [[ $# -gt 0 ]]; do
        case $1 in
            --force)
                FORCE=1
                shift
                ;;
            --no-editable)
                NO_EDITABLE=1
                shift
                ;;
            *)
                echo "Unknown venv option: $1"
                exit 1
                ;;            
        esac
    done


    if [ "$FORCE" = "1" ] && [ -d .venv ]; then
        echo "Removing existing virtual environment..."
        rm -rf .venv
    fi

    if [ -d .venv ] ; then
        return 0
    fi

    echo "Setting up virtual environment with Python $PYTHON and oarepo version $OAREPO_VERSION"
    uv venv --python=$PYTHON --seed
    source .venv/bin/activate

    uv pip install setuptools
    uv pip install "oarepo[rdm,tests]>=${OAREPO_VERSION},<$(($OAREPO_VERSION + 1))"

    if [ -z "$NO_EDITABLE" ]; then
        echo "Installing the package in editable mode."
        uv pip install -e '.[tests]'
    else
        echo "Building and Installing the package."
        if [ -d dist ]; then
            echo "Removing existing dist directory..."
            rm -rf dist
        fi
        uv build --wheel
        wheel_package=$(ls dist/*.whl | head -n 1)
        uv pip install "${wheel_package}[tests]"
    fi
}

run_tests() {
    set -e
    set -o pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-services)
                SKIP_SERVICES=1
                shift
                ;;
            --with-coverage)
                WITH_COVERAGE=1
                shift
                ;;
            *)
                echo "Unknown test option: $1"
                exit 1
                ;;
        esac
    done

    setup_venv

    if [ -f ./test-setup.sh ]; then
        echo "Sourcing test setup script..."
        ./test-setup.sh
    else
        echo "No test-setup.sh found, skipping extra test setup."
    fi

    if [ -z "$SKIP_SERVICES" ]; then
        start_services
    fi

    if [ ! -z "$WITH_COVERAGE" ]; then
        echo "Enabling coverage for tests..."
        uv pip install pytest-cov
        export PYTEST_ADDOPTS="--cov=${code_directories[0]} --cov-report=json --cov-report=html --cov-report=term-missing:skip-covered"
        echo "Running tests with coverage enabled, opts are: $PYTEST_ADDOPTS"
    fi
    source .venv/bin/activate
    source .env-services
    pytest "$@"
}

cleanup() {
    set -e
    set -o pipefail    

    echo "Stopping services..."
    stop_services

    if [ -d .venv ]; then
        echo "Removing virtual environment..."
        rm -rf .venv
    fi

    if [ -f .env-services ]; then
        echo "Removing environment file..."
        rm -f .env-services
    fi

    echo "Cleanup completed."
}

self_update() {
    set -euo pipefail

    echo "Updating runner script..."
    curl --fail -o "./.runner-new.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/runner.sh
    chmod +x "./.runner-new.sh"
    if "./.runner-new.sh" check-script-working ; then
        mv "./.runner-new.sh" "./.runner.sh"
        echo "Runner script updated successfully."
    else
        echo "New runner script is not working, keeping the old one."
        rm "./.runner-new.sh"
    fi
    return 0
}

check_license_headers() {
    set -e
    set -o pipefail

    if [ -f .check_ok.txt ]; then
        rm .check_ok.txt
    fi
    if [ -f .check_errors.txt ]; then
        rm .check_errors.txt
    fi
    touch .check_ok.txt
    touch .check_errors.txt
    # Check for license headers in Python files
    find ${code_directories[@]} -name "*.py" | while read -r file; do
        if cat $file | grep -i "Copyright (c)" >/dev/null; then
            echo "$file" >>.check_ok.txt
        else
            echo "Missing license header in $file"
            cat $file | grep -i "Copyright (c)"
            echo "$file" >>.check_errors.txt
        fi
    done

    ok=$(wc -l < .check_ok.txt)
    errors=$(wc -l < .check_errors.txt)

    rm .check_ok.txt
    rm .check_errors.txt

    if [ $errors -gt 0 ]; then
        echo "${errors} file(s) are missing license headers."
        return 1
    fi
}

check_future_annotations() {
    set -e
    set -o pipefail

    if [ -f .check_ok.txt ]; then
        rm .check_ok.txt
    fi
    if [ -f .check_errors.txt ]; then
        rm .check_errors.txt
    fi
    touch .check_ok.txt
    touch .check_errors.txt

    # Check for future annotations in Python files
    find ${code_directories[@]} -name "*.py" -not -path "./.venv/*" | while read -r file; do
        if cat $file | grep "from __future__" | grep "annotations" >/dev/null; then
            echo "$file" >>.check_ok.txt
        else
            echo "Missing 'from __future__ import annotations' in $file"
            echo "$file" >>.check_errors.txt
        fi
    done

    ok=$(wc -l < .check_ok.txt)
    errors=$(wc -l < .check_errors.txt)

    rm .check_ok.txt
    rm .check_errors.txt

    if [ $errors -gt 0 ]; then
        echo "${errors} file(s) are missing future annotations."
        return 1
    fi
}

run_linters() {
    set -e
    set -o pipefail

    setup_venv

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

    uvx -p python3.13 ruff check --exclude pyproject.toml
    uvx -p python3.13 ruff format --check --exclude pyproject.toml
    check_license_headers
    check_future_annotations

    cat <<EOF >.mypy.ini
[mypy]
warn_return_any = True
warn_unused_configs = True
warn_unreachable = True
follow_untyped_imports = True
EOF
    uvx --with types-PyYAML -p .venv/bin/python mypy "${code_directories[0]}" --ignore-missing-imports
    uvx pyright --pythonpath .venv/bin/python "${code_directories[0]}"
}

format_code() {
    set -e
    set -o pipefail

    uvx ruff format --exclude pyproject.toml
    uvx ruff check --fix --exclude pyproject.toml
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
EOF

    # run eslint
    echo "Running ESLint..."
    node_modules/.bin/eslint --ext .js,.jsx,.ts,.tsx --fix "${code_directories[@]}"

    # run prettier
    echo "Running Prettier..."
    node_modules/.bin/prettier --write "${code_directories[@]}"

    return 0
}


add_license_headers() {
    set -e
    set -o pipefail

    current_year=$(date +%Y)
    ORGANIZATION=${ORGANIZATION:-"CESNET z.s.p.o"}
    home_page=$(get_home_page)

    cat <<'EOF' > /tmp/license-header.txt
Copyright (c) ${years} ${owner}.

This file is a part of ${projectname} (see ${projecturl}).

${projectname} is free software; you can redistribute it and/or modify it
under the terms of the MIT License; see LICENSE file for more details.
EOF

    find ${code_directories[*]} -name "*.py" -not -path "./.venv/*" | while read -r file; do
        if ! cat $file | grep -iq "Copyright (C)"; then
            uvx licenseheaders -t /tmp/license-header.txt -y $current_year \
                -o "$ORGANIZATION" -n $package_name \
                -u $home_page -f $file
        fi
    done
}

# run the tools and exit to prevent evaluation after this line in case the script
# is self updated
run_tools "$@"; exit;
