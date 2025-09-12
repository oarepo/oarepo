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
export MODEL_TEMPLATE=${MODEL_TEMPLATE:-"https://github.com/oarepo/nrp-model-copier"}
export MODEL_TEMPLATE_VERSION=${MODEL_TEMPLATE_VERSION:-"rdm-13"}
export LC_TIME=${LC_TIME:-"en_US.UTF-8"}

show_help() {
    echo "Usage: run.sh command [options]"
    echo ""
    echo "Commands:"
    echo "  install                    Install the repository"
    echo "  services setup             Setup docker services"
    echo "  services start             Start docker services"
    echo "  services stop              Stop docker services"
    echo "  model create [config-file]   Create a new record model"
    echo "  run [--no-services]        Run the repository"
    echo
    echo "  self-update                Update the runner script to the latest version"
    echo "Options:"
    echo "  --help                     Show this help message"
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


# shellcheck disable=SC2120
in_invenio_shell() {
    set -e
    set -o pipefail

    export PYTHON_BASIC_REPL=0
    if [ -t 0 ]; then
        # stdin is a terminal, so take args instead
        cmd="$*"
    else
        cmd=$(cat)
    fi

    uv run invenio shell --no-term-title -c "${cmd}"
}


run_invenio_cli() {
    set -euo pipefail

    # temporary implementation until release
    uvx \
        --with git+https://github.com/oarepo/oarepo-cli@rdm-13 \
        --from git+https://github.com/oarepo/invenio-cli@oarepo-feature-docker-environment \
        invenio-cli "$@"
}

install_repository() {
    instance_path=$(echo "print(app.instance_path, end='')" | in_invenio_shell | tail -n1)
    assets_path="${instance_path}/assets"

    # TODO: need to sync before the installation as I need to call invenio to register
    # less components. This should be put directly into the install as an extra step
    # after the project is installed and before the collect is called.
    uv sync

    # TODO: update nrp-cli to use correct config-file
    run_invenio_cli install

    echo "Configuring local service ports in .invenio.private"
    source variables
    (
        cat .invenio.private | sed -E '/^(search|db|redis|rabbitmq|s3|web)_port/d'
        echo "search_port = ${INVENIO_OPENSEARCH_PORT}"
        echo "db_port = ${INVENIO_DATABASE_PORT}"
        echo "redis_port = ${INVENIO_REDIS_PORT}"
        echo "rabbitmq_port = ${INVENIO_RABBIT_PORT}"
        echo "s3_port = ${INVENIO_S3_PORT}"
        echo "web_port = ${INVENIO_UI_PORT}"
    ) > .invenio.private.tmp

    mv .invenio.private.tmp .invenio.private
}

model() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            create)
                create_model $2
                return 0
                ;;
            *)
                echo "Unknown model option $1"
                show_help
                exit 1
        esac
    done
}    

create_model() {
    set -euo pipefail
    model_config_file=$1
    shift

    if [ ! -f "${model_config_file}" ]; then
        echo "Missing model config: ${model_config_file}"
        exit 1
    fi

    # if template starts with https, it is a github url
    if [[ "${MODEL_TEMPLATE}" == https://* ]]; then
        echo "Using template from GitHub: ${MODEL_TEMPLATE} with version ${MODEL_TEMPLATE_VERSION}"
        uvx --with tomli --with tomli-w --with copier-templates-extensions \
            copier copy --trust --vcs-ref ${MODEL_TEMPLATE_VERSION}\
            --data-file "${model_config_file}" \
            "${MODEL_TEMPLATE}" . "${@}"
    else
        echo "Using local template: ${MODEL_TEMPLATE}"
        uvx --with tomli --with tomli-w --with copier-templates-extensions\
            copier copy --trust\
            --data-file "${model_config_file}" \
            "${MODEL_TEMPLATE}" . "${@}"
    fi

    if [ -d ".venv" ]; then
        install_repository
    fi
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
    export PYTHONWARNINGS=ignore
    source .venv/bin/activate
    invenio "$@"
}

run() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help)
                show_help
                exit 0
                ;;
            install)
                install_repository
                exit 0
                ;;
            model)
                shift
                model "$@"
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
            run)
                run_server
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