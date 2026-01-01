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

# needed for osx to get DYLD_LIBRARY_PATH working
if [ -f ~/.envrc.local ] ; then
    # shellcheck disable=SC1090
    source ~/.envrc.local
fi

export UV_EXTRA_INDEX_URL=${UV_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
# Allow resolution & installation of RDM packages with pre-release versioning, e.g: `invenio-app-rdm==14.0.0.68614b0.dev3`
export UV_PRERELEASE=${UV_PRERELEASE:-"allow"}
export PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export MODEL_TEMPLATE=${MODEL_TEMPLATE:-"https://github.com/oarepo/nrp-model-copier"}
export MODEL_TEMPLATE_VERSION=${MODEL_TEMPLATE_VERSION:-"rdm-14"}
export LC_TIME=${LC_TIME:-"en_US.UTF-8"}
export UV_PROJECT_ENVIRONMENT=${UV_PROJECT_ENVIRONMENT:-".venv"}

# MacOS workaround for crashing celery workers
if [[ "$OSTYPE" == "darwin"* ]]; then
    export INVENIO_CELERY_WORKER_POOL=threads
    export INVENIO_CELERY_WORKER_CONCURRENCY=4
    # alternative:
    # export OBJC_DISABLE_INITIALIZE_FORK_SAFETY="YES"
    # export INVENIO_CELERY_WORKER_POOL="solo"
fi

# region: Python version detection
get_python_versions_from_pyproject() {
    # Parse requires-python from pyproject.toml to get supported Python versions
    if [ ! -f pyproject.toml ]; then
        echo "No pyproject.toml found in the current directory." >&2
        exit 1
    fi
    
    local requires_python
    requires_python=$(grep 'requires-python' pyproject.toml | head -n 1 || echo "")
    
    if [ -z "$requires_python" ]; then
        echo "No 'requires-python' field found in pyproject.toml." >&2
        exit 1
    fi
    
    # Extract version constraints (e.g., ">=3.12,<3.15" or ">=3.12")
    local version_string
    version_string=$(echo "$requires_python" | sed 's/.*>=//' | sed 's/["<].*//')
    
    local lower_bound
    lower_bound=$(echo "$version_string" | cut -d',' -f1 | sed 's/3\.//')
    
    # Check if there's an upper bound
    local upper_bound
    if echo "$requires_python" | grep -q '<'; then
        upper_bound=$(echo "$requires_python" | sed 's/.*<//' | sed 's/".*//' | sed 's/3\.//')
        upper_bound=$((upper_bound - 1))
    else
        echo "No upper bound found; please add <3.15 into the requires-python field in pyproject.toml." >&2
        exit 1
    fi
    
    # Generate list of versions
    local versions=()
    for minor in $(seq "$lower_bound" "$upper_bound"); do
        versions+=("3.$minor")
    done
    
    echo "${versions[@]}"
}

get_highest_available_python() {
    # Get python versions from pyproject.toml
    local python_versions
    python_versions=$(get_python_versions_from_pyproject)
    
    # Temporarily deactivate virtual environment if active to check system Python versions
    local was_in_venv=0
    local old_path="$PATH"
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        was_in_venv=1
        # Remove venv paths from PATH
        PATH=$(echo "$PATH" | tr ':' '\n' | grep -v "$VIRTUAL_ENV" | tr '\n' ':' | sed 's/:$//')
        unset VIRTUAL_ENV
    fi
    
    # Try each version from highest to lowest
    local highest_version=""
    local highest_minor=0
    
    for version in $python_versions; do
        # Check if this python version exists on the system
        if command -v "python${version}" >/dev/null 2>&1; then
            # Extract minor version number for comparison (e.g., "3.14" -> 14)
            local minor
            minor=$(echo "$version" | cut -d'.' -f2)
            if [ "$minor" -gt "$highest_minor" ]; then
                highest_minor=$minor
                highest_version=$version
            fi
        fi
    done
    
    # Restore PATH if we modified it
    if [ "$was_in_venv" -eq 1 ]; then
        PATH="$old_path"
    fi
    
    if [ -z "$highest_version" ]; then
        echo "No compatible Python version found on the system." >&2
        echo "Required versions according to pyproject.toml: $python_versions" >&2
        echo "Please install one of the required Python versions." >&2
        exit 1
    fi
    
    echo "python${highest_version}"
}

# Detect and set Python version
if [ -z "${PYTHON:-}" ]; then
    export PYTHON=$(get_highest_available_python)
fi
# endregion: Python version detection

show_help() {
    echo "Usage: run.sh command [options]"
    echo ""
    echo "Commands:"
    echo "  install                    Install the repository"
    echo "  upgrade                    Upgrade the repository (clean cache and reinstall)"
    echo "  services setup             Setup docker services"
    echo "  services start             Start docker services"
    echo "  services stop              Stop docker services"
    echo "  model create [model-name] [config-file]   Create a new record model."
    echo "      Config file is optional."
    echo "  model update [model-name] [answers-file] Update an existing record model."
    echo "      Answers file is optional."
    echo "  info                       Show Python version and models information"
    echo "  local add <path>           Add a local package to tool.uv.sources"
    echo "  local remove <name|--all>  Remove a local package or all from tool.uv.sources"
    echo "  run                        Run the repository"
    echo "      [--no-services]        Do not start docker services"
    echo "      [--no-celery]          Do not start background tasks"
    echo "  cli [subcommand]           Run the invenio-cli command"
    echo
    echo "  self-update                Update the runner script to the latest version"
    echo "  translations init <lang>   Initialize backend translations for the given language"
    echo "  translations extract       Extract backend translations"
    echo "  translations update        Update backend translations"
    echo "  translations compile       Compile backend translations"
    echo "  jstranslations extract     Extract frontend (JS) translations"
    echo "Options:"
    echo "  --help                     Show this help message"
}

local_sources_cmd() {
    set -euo pipefail
    local subcmd="$1"; shift || true
    local pyproject="pyproject.toml"
    if [ ! -f "$pyproject" ]; then
        echo "pyproject.toml not found in current directory" >&2
        exit 1
    fi
    case "$subcmd" in
        add)
            shift
            if [ $# -lt 1 ]; then
                echo "Usage: $0 local add <path>" >&2
                exit 1
            fi
            local pkgdir="$1"
            shift
            if [ ! -f "$pkgdir/pyproject.toml" ]; then
                echo "No pyproject.toml in $pkgdir" >&2; exit 1
            fi
            uv add "$pkgdir" --editable "$@"
            upgrade_repository
        ;;
        remove)
            echo "Removing local package from tool.uv.sources is not yet implemented." >&2
            echo "Please remove them manually from pyproject.toml" >&2
            echo "and then run ./run.sh upgrade" >&2
            exit 1
            ;;
        *)  
            echo "Usage: $0 local [add <path>|remove]" >&2
            exit 1
            ;;
    esac
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

show_info() {
    set -euo pipefail

    echo "Python version: $PYTHON"
    "$PYTHON" --version
    echo ""
    echo "Models:"
    
    # Find all directories containing .copier-answers.yml
    local found_models=0
    for dir in */; do
        if [ -f "${dir}.copier-answers.yml" ] && [ -f "${dir}model.py" ]; then
            found_models=1
            local model_name="${dir%/}"
            
            # Extract version from model.py
            local version
            version=$(grep -E 'version\s*=\s*["\x27]' "${dir}model.py" | head -n 1 | sed -E 's/.*version\s*=\s*["\x27]([^"\x27]+)["\x27].*/\1/' || echo "unknown")
            
            echo "  - $model_name: $version"
        fi
    done
    
    if [ "$found_models" -eq 0 ]; then
        echo "  No models found."
    fi
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
    uvx --python="$PYTHON" \
        --with git+https://github.com/oarepo/oarepo-cli@rdm-14 \
        --from git+https://github.com/oarepo/invenio-cli@oarepo-feature-docker-environment \
        invenio-cli "$@"
}

install_repository() {
    # TODO: need to sync before the installation as I need to call invenio to register
    # less components. This should be put directly into the install as an extra step
    # after the project is installed and before the collect is called.
    uv sync --python="$PYTHON" 

    instance_path=$(echo "print(app.instance_path, end='')" | in_invenio_shell | tail -n1)
    assets_path="${instance_path}/assets"

    echo "Installing repository in virtual environment: ${UV_PROJECT_ENVIRONMENT}"
    echo "Instance path: ${instance_path}"
    echo "Assets path: ${assets_path}"
    if [ ! -d ${instance_path} ]; then
        echo "Creating instance path: ${instance_path}"
        mkdir -p "${instance_path}"
    fi
    if [ ! -f ${instance_path}/invenio.cfg ]; then
        ln -s $PWD/invenio.cfg "${instance_path}/invenio.cfg" || true
    fi

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

upgrade_repository() {
    set -euo pipefail

    echo "Upgrading repository..."
    
    # Remove .venv if it exists
    if [ -d .venv ]; then
        echo "Removing virtual environment..."
        rm -rf .venv
    fi
    
    # Remove uv.lock if it exists
    if [ -f uv.lock ]; then
        echo "Removing uv.lock..."
        rm -f uv.lock
    fi
    
    # Clean uv cache
    echo "Cleaning uv cache..."
    uv cache clean --force
    
    # Reinstall repository
    echo "Reinstalling repository..."
    install_repository
    
    echo "Upgrade completed successfully."
}

model() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            create)
                shift
                create_model "$@"
                return 0
                ;;
            update)
                shift
                update_model "$@"
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
    if [ $# -eq 0 ]; then
        echo "Model name is required."
        exit 1
    fi
    model_name="$1"
    shift
    if [ $# -eq 0 ]; then
        # if template starts with https, it is a github url
        if [[ "${MODEL_TEMPLATE}" == https://* ]]; then
            echo "Using template from GitHub: ${MODEL_TEMPLATE} with version ${MODEL_TEMPLATE_VERSION}"
            uvx --python="$PYTHON" --with tomli --with tomli-w --with copier-templates-extensions \
                copier copy --trust --vcs-ref ${MODEL_TEMPLATE_VERSION} \
                -d model_name="${model_name}" \
                "${MODEL_TEMPLATE}" . 
        else
            echo "Using local template: ${MODEL_TEMPLATE}"
            uvx --python="$PYTHON" --with tomli --with tomli-w --with copier-templates-extensions \
                copier copy --trust \
                -d model_name="${model_name}" \
                "${MODEL_TEMPLATE}" . 
        fi
    else
        model_config_file="$1"
        shift

        if [ ! -f "${model_config_file}" ]; then
            echo "Missing model config file: ${model_config_file}"
            exit 1
        fi

        # if template starts with https, it is a github url
        if [[ "${MODEL_TEMPLATE}" == https://* ]]; then
            echo "Using template from GitHub: ${MODEL_TEMPLATE} with version ${MODEL_TEMPLATE_VERSION}"
            uvx --python="$PYTHON" --with tomli --with tomli-w --with copier-templates-extensions \
                copier copy --trust --vcs-ref ${MODEL_TEMPLATE_VERSION}\
                --answers-file "${model_config_file}" \
                "${MODEL_TEMPLATE}" . "${@}"
        else
            echo "Using local template: ${MODEL_TEMPLATE}"
            uvx --python="$PYTHON" --with tomli --with tomli-w --with copier-templates-extensions\
                copier copy --trust\
                --answers-file "${model_config_file}" \
                "${MODEL_TEMPLATE}" . "${@}"
        fi
    fi

    if [ -d ".venv" ]; then
        install_repository
    fi
}

# update model works based on .copier-answers.yml, so if you wish to use a local template
# you would need to pass specific config file where you specify the template to be used
update_model() {
    set -euo pipefail
    if [ $# -eq 0 ]; then
        echo "Missing model name for update."
        exit 1
    fi

    model_name="$1"
    shift

    if [ ! -d "${model_name}" ]; then
        echo "Model directory '${model_name}' does not exist."
        exit 1
    fi

    answers_file="./${model_name}/.copier-answers.yml"

    if [ $# -ge 1 ]; then
         model_config_file="$1"
    if [ -f "${model_config_file}" ]; then
        answers_file="${model_config_file}"
    else
        echo "Model config file does not exist: ${model_config_file}"
        exit 1
        fi
    fi
    
    echo "answers file: ${answers_file}"
    if [ ! -f "${answers_file}" ]; then
        echo "Answers file '${answers_file}' does not exist."
        exit 1
    fi


    echo "Updating template from GitHub: ${MODEL_TEMPLATE} with version ${MODEL_TEMPLATE_VERSION} with answers file ${answers_file}"
    uvx --python="$PYTHON" --with pycountry --with tomli --with tomli-w --with copier-templates-extensions \
        copier update --trust --vcs-ref ${MODEL_TEMPLATE_VERSION} --conflict inline \
        --answers-file "${answers_file}" 

}

services() {
    set -euo pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            setup)
                shift
                run_invenio_cli services setup "$@"
                return 0
                ;;
            start)
                shift
                run_invenio_cli services start "$@"
                return 0
            ;;
            stop)
                shift
                run_invenio_cli services stop "$@"
                return 0
            ;;
            *)
                echo "Unknown services option $1"
                show_help
                exit 1
        esac
    done
}

compile_be_translations() {
    set -euo pipefail

    if [ -d .venv ] ; then source .venv/bin/activate ; fi
    run_invenio_cli translations compile
}

extract_be_translations() {
    set -euo pipefail

    if [ -d .venv ] ; then source .venv/bin/activate ; fi
    run_invenio_cli translations extract
}

update_be_translations() {
    set -euo pipefail

    if [ -d .venv ] ; then source .venv/bin/activate ; fi
    run_invenio_cli translations update
}

initialize_be_translations() {
    set -euo pipefail

    if [ $# -eq 0 ]; then
        echo "Language code is required."
        echo "Usage: ./run.sh translations init <language-code>"
        echo "Example: ./run.sh translations init cs"
        exit 1
    fi

    if [ -d .venv ] ; then source .venv/bin/activate ; fi
    run_invenio_cli translations init -l "$1"
}

extract_js_translations() {
    set -euo pipefail
    cd i18n/semantic-ui/translations
    npm install
    npm run extract_messages
}

translations() {
    set -euo pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            init)
                shift
                initialize_be_translations "$@"
                return 0
                ;;
            extract)
                shift
                extract_be_translations
                return 0
                ;;
            update)
                shift
                update_be_translations
                return 0
                ;;
            compile)
                shift
                compile_be_translations
                return 0
                ;;
            *)
                echo "Unknown translations option: $1"
                echo "Usage: ./run.sh translations [init <lang>|extract|update|compile]"
                exit 1
                ;;
        esac
    done

    echo "Usage: ./run.sh translations [init <lang>|extract|update|compile]"
    exit 1
}

jstranslations() {
    set -euo pipefail

    while [[ $# -gt 0 ]]; do
        case $1 in
            extract)
                shift
                extract_js_translations
                return 0
                ;;
            *)
                echo "Unknown jstranslations option: $1"
                echo "Usage: ./run.sh jstranslations extract"
                exit 1
                ;;
        esac
    done

    echo "Usage: ./run.sh jstranslations extract"
    exit 1
}


run_server() {
    set -euo pipefail

    no_services=0
    no_celery=0
    extra_options=()
    export INVENIO_SITE_CERT_PATH="$PWD/docker/development.crt"
    export INVENIO_SITE_KEY_PATH="$PWD/docker/development.key"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-services)
                no_services=1
                shift
                ;;
            --no-celery)
                no_celery=1
                shift
                ;;
            *)
                extra_options+=("$1")
                shift
                ;;
        esac
    done

    if [[ $no_services -eq 0 ]]; then
        services start
    fi

    if [[ $no_celery -eq 0 ]]; then
        # start celery worker in the background
        run_invenio_cli run ${extra_options[@]}
    else
        export FLASK_DEBUG=1 
        export PYTHONWARNINGS=ignore
        if [ -d .venv ] ; then source .venv/bin/activate ; fi
        invenio run --cert ./docker/development.crt --key ./docker/development.key ${extra_options[@]}
    fi
}

run_invenio() {
    export PYTHONWARNINGS=ignore
    if [ -d .venv ] ; then source .venv/bin/activate ; fi
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
            upgrade)
                upgrade_repository
                exit 0
                ;;
            translations)
                shift
                translations "$@"
                exit 0
                ;;
            jstranslations)
                shift
                jstranslations "$@"
                exit 0
                ;;
            info)
                show_info
                exit 0
                ;;
            model)
                shift
                model "$@"
                exit 0
                ;;
            local)
                shift
                local_sources_cmd "$@"
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
            cli)
                shift
                run_invenio_cli "$@"
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