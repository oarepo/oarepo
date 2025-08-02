#!/usr/bin/env bash
#
# This script sets up a Python virtual environment, installs necessary packages,
# runs tests and other tasks for libraries which are part of the OARepo Invenio RDM
# flavour.
# 
# Usage: ./run --help
#
# Note: To ensure consistency, this script is not part of the library. 
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

base_dir="$(dirname "$0")"

run_tools() {
    set -e
    set -o pipefail    
    
    # Parse the commandline according to the options defined above.
    OAREPO_VERSION=${OAREPO_VERSION:-"13"}
    PYTHON_VERSION=${PYTHON_VERSION:-"3.13"}
    PYTHON=${PYTHON:-"python${PYTHON_VERSION}"}
    TASK_NAME=${TASK_NAME:-""}

    while [[ $# -gt 0 ]]; do
        case $1 in
            venv)
                FORCE=1 setup_venv
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
                setup_venv
                start_services
                source .venv/bin/activate
                source .env-services
                bash
                return 0
                ;;
            invenio)
                shift
                setup_venv
                start_services
                source .venv/bin/activate
                source .env-services
                invenio "$@"
                return 0
                ;;
            translations)
                shift
                uvx --from oarepo-tools make-translations
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
            --skip-services)
                SKIP_SERVICES=1
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
    echo "  start             Start the services for testing"
    echo "  stop              Stop the services after testing"
    echo "  test              Run the tests"
    echo "  oarepo-versions   List the supported OARepo versions for this package"
    echo "  clean             Clean up the environment (stop services, remove venv, etc.)"
    echo "  shell             Start a shell with the virtual environment and services running"
    echo "  invenio           Run an Invenio command with the virtual environment and services running"
    echo "  translations      Extract/compile translations for this package"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  OAREPO_VERSION    The version of OARepo to use (default: 13)"
    echo "  PYTHON_VERSION    The Python interpreter to use (default: 3.13)"
    echo "  PYTHON            The Python executable to use (default: python3.13)"
    echo ""
    echo "Options:"
    echo "  --skip-services   Skip starting/stopping services"
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

    eval "$(uvx docker-services-cli down --env)"
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

    uvx docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-opensearch} --mq ${MQ:-rabbitmq} --cache ${CACHE:-redis} --env > .env-services
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
        get_python_versions "$python_version_string"
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
    version_string=$(echo "$1" | sed 's/.*>=//' | sed 's/".*//')
    lower_bound=$(echo "$version_string" | cut -d',' -f1 | sed 's/^3\.//')
    upper_bound=$(echo "$version_string" | cut -d',' -f2 | sed 's/<//' | sed 's/^3\.//')
    if [ -z "$upper_bound" ]; then
        upper_bound=$((lower_bound + 1))
    fi
    upper_bound=$((upper_bound - 1))
    versions=$(seq "$lower_bound" "$upper_bound")
    versions=$(echo "$versions" | sed 's/^/"3./' | sed 's/$/"/' | tr '\n' ',' | sed 's/,$//')
    echo -n "[$versions]"
}

setup_venv() {
    set -e
    set -o pipefail    

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

    uv pip install "oarepo[rdm,tests]>=${OAREPO_VERSION},<$(($OAREPO_VERSION + 1))"
    uv pip install '.[tests]'
}

run_tests() {
    set -e
    set -o pipefail
    setup_venv
    start_services
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
    set -e
    set -o pipefail

    echo "Updating runner script..."
    curl --fail -o "${base_dir}/.runner-new.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/runner.sh
    chmod +x "${base_dir}/.runner-new.sh"
    if "${base_dir}/.runner-new.sh" check-script-working ; then
        mv "${base_dir}/.runner-new.sh" "${base_dir}/.runner.sh"
        echo "Runner script updated successfully."
    else
        echo "New runner script is not working, keeping the old one."
        rm "${base_dir}/.runner-new.sh"
    fi
    return 0
}

# run the tools and exit to prevent evaluation after this line in case the script
# is self updated
run_tools "$@"; exit;
