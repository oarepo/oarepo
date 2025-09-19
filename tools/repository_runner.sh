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
    echo "  services setup        Setup docker services"
    echo "  services start        Start docker services"
    echo "  services stop         Stop docker services"
    echo "  run [--no-services]   Run the repository"
    echo ""
    echo "  model add <name>      Add a new model"
    echo "     --template         Path to the model template directory"
    echo "     --version          Version of the model template."
    echo "     --with-ccmm        Add the Czech Core Metadata Model support."
    echo
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
    # TODO: need to sync before the installation as I need to call invenio to register
    # less components. This should be put directly into the install as an extra step
    # after the project is installed and before the collect is called.
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
                return 0
                ;;
            start)
                run_invenio_cli services start
                return 0
            ;;
            stop)
                run_invenio_cli services stop
                return 0
            ;;
            *)
                echo "Unknown services option $1"
                show_help
                exit 1
        esac
    done
}

run_server() {
    set -euo pipefail

    no_services=0

    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-services)
                no_services=1
                shift
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    if [[ $no_services -eq 0 ]]; then
        services start
    fi

    export FLASK_DEBUG=1 
    export PYTHONWARNINGS=ignore
    source .venv/bin/activate
    invenio run --cert ./docker/development.crt --key ./docker/development.key
}

run_invenio() {
    set -euo pipefail

    export PYTHONWARNINGS=ignore
    source .venv/bin/activate
    invenio "$@"
}

model_commands() {
    set -euo pipefail
    echo "Model commands $@"
    while [[ $# -gt 0 ]]; do
        case $1 in
            add)
                shift
                add_new_model "$@"
                return 0
                ;;
            *)
                echo "Unknown model command: $1"
                show_help
                exit 1
                ;;
        esac
    done

    echo "Model command required"
    show_help
    exit 1
}

add_new_model() {
    set -euo pipefail
    set -x

    vcs_ref="rdm13"
    template="https://github.com/oarepo/nrp-model-copier"
    model_name=""
    parameters=()

    while [[ $# -gt 0 ]]; do
        case $1 in
            --version)
                shift
                if [[ $# -lt 1 ]]; then
                    echo "--version requires a value."
                    show_help
                    exit 1
                fi
                vcs_ref=$1
                shift
                ;;
            --template)
                shift
                if [[ $# -lt 1 ]]; then
                    echo "--template requires a value."
                    show_help
                    exit 1
                fi
                template=$1
                shift
                ;;
            --with-ccmm)
                with_ccmm=true
                parameters+=("-d" 'ccmm=true')
                shift
                ;;
            *)
                if [ -z "$model_name" ] ;
                then
                    model_name=$1
                    shift
                else
                    echo "Model name already specified: $model_name"
                    show_help
                    exit 1
                fi
                ;;
        esac
    done

    if [ -z "$model_name" ]; then
        echo "Model name is required."
        show_help
        exit 1
    fi

    parameters+=("-d" "model_name:$1")
    parameters+=("--vcs-ref" "$1")

    uvx \
        --with tomli --with tomli-w \
        --with copier-templates-extensions \
        copier copy --trust $template \
        "${parameters[@]}" \
        .
}

run() {
    set -euo pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            --help)
                show_help
                exit 0
                ;;
            install)
                shift
                install "$@"
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
            model)
            shift
                model_commands "$@"
                exit 0
                ;;
            build)
                shift
                build_repository "$@"
                exit 0
                ;;
            run)
                shift
                run_server "$@"
                exit 0
                ;;
            invenio)
                shift
                run_invenio "$@"
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