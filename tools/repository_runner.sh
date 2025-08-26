#!/usr/bin/env bash
#
# This script is used as a high-level tool that builds and runs an Invenio NRP
# (Czech National Repository Platform) repository.
# 
# Usage: ./run --help
#
# Note: To ensure consistency, this script is never committed to the repository.
# Only the stub (run.sh) should be placed in the repository directory.
# The actual script is downloaded from the OARepo repository on the first run and cached.
# as .runner.sh. If you want to update the script, run ./run.sh self-update.
#
# (C) 2025 CESNET, z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#

set -euo pipefail

export UV_EXTRA_INDEX_URL=${UV_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export LC_TIME=${LC_TIME:-"en_US.UTF-8"}

show_help() {
    echo "Usage: run.sh command [options]"
    echo ""
    echo "Commands:"
    echo "  install               Install the repository"
    echo "  self-update           Update the runner script to the latest version"
    echo "Options:"
    echo "  --help                Show this help message"
}

self_update() {
    set -euo pipefail

    echo "Updating runner script..."
    curl --fail -o "./.runner-new.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/repository_runner.sh
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

run_invenio_cli() {
    set -euo pipefail

    # temporary implementation until release
    uvx \
        --with git+https://github.com/oarepo/oarepo-cli@rdm-13 \
        --from git+https://github.com/oarepo/invenio-cli@oarepo-feature-docker-environment \
        invenio-cli "$@"
}

install() {
    set -euo pipefail
    uv sync
    run_invenio_cli less register
    run_invenio_cli install
}

services() {
    set -euo pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            setup)
                run_invenio_cli services setup
                exit 0
                ;;
            *)
                echo "Unknown services option $1"
                show_help
                exit 1
        esac
    done
}

run() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help)
                show_help
                exit 0
                ;;
            install)
                install
                exit 0
                ;;
            services)
                shift
                services "$@"
                exit 0
                ;;
            self-update)
                self_update
                exit 0
                ;;
            build)
                build_repository
                exit 0
                ;;
            check-script-working)
                # This is used to check if the script is working after self-update.
                # It should return 0 if the script is working, 1 otherwise.
                echo "Script is working."
                return 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
        shift
    done
    show_help
    exit 0
}

run "$@"; exit 0;