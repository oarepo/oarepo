#!/usr/bin/env bash

#
# This script installs an Invenio NRP (Cech National Repository Platform) repository
#
# Usage: ./repository_installer.sh <options> REPOSITORY_NAME
#
# Options:
#
# --python <python_binary>  Specify the Python binary to use (default: python3.13)
# --template <template>     Default is https://github.com/oarepo/nrp-app-copier . 
#                           Specify either a https github URL or a local path to a template.
# --version <rdm-14>        Specify the version of the template if it is a github URL.
# --uv <uv_binary>          Specify the uv binary to use (default: uv).
#

set -euo pipefail

python_binary="python3.13"
template="https://github.com/oarepo/nrp-app-copier"
version="rdm-14"
uv_binary="uv"
uvx_binary="uvx"
repository_name=""
copier_arguments=()

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --config)
                copier_arguments+=("--data-file" "$2")
                shift 2
                ;;
            --python)
                python_binary="$2"
                shift 2
                ;;
            --template)
                template="$2"
                shift 2
                ;;
            --version)
                version="$2"
                shift 2
                ;;
            --uv)
                uv_binary="$2"
                shift 2
                ;;
            --uvx)
                uvx_binary="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                if [[ -z "${repository_name}" ]]; then
                    repository_name="$1"
                else
                    echo "Unknown option: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # check if the uv command works
    if ! command -v "${uv_binary}" &> /dev/null; then
        echo "Error: uv command not found. "
        echo "Please install uv from https://docs.astral.sh/uv/getting-started/installation/"
        echo "or specify a path to the binary with --uv option."
        exit 1
    fi

    # check if the uvx command works
    if ! command -v "${uvx_binary}" &> /dev/null; then
        echo "Error: uvx command not found. "
        echo "Please install uvx from https://docs.astral.sh/uv/getting-started/installation/"
        echo "or specify a path to the binary with --uvx option."
        exit 1
    fi

    # check if the python binary works
    if ! command -v "${python_binary}" &> /dev/null; then
        echo "Error: Python binary '${python_binary}' not found. Please install Python or specify a different binary with --python option."
        exit 1
    fi

    # check if the repository name is provided
    if [[ -z "${repository_name:-}" ]]; then
        echo "Error: Repository name is required."
        show_help
        exit 1
    fi
}

show_help() {
    echo "Usage: $0 <options> REPOSITORY_NAME"
    echo ""
    echo "Options:"
    echo "  --config config_file      Specify initial config"
    echo
    echo "  --python <python_binary>  Specify the Python binary to use (default: python3.13)"
    echo "  --template <template>     Default is https://github.com/oarepo/nrp-app-copier"
    echo "  --version <rdm-14>        Specify the version of the template if it is a github URL."
    echo "  --uv <uv_binary>          Specify the uv binary to use (default: uv)."
    echo "  --uvx <uvx_binary>       Specify the uvx binary to use (default: uvx)."
}

create_repository() {
    set -euo pipefail

    # if template starts with https, it is a github url
    if [[ "${template}" == https://* ]]; then
        echo "Using template from GitHub: ${template} with version ${version}"
        uvx --python "${python_binary}" \
            --with copier-template-extensions --with pycountry \
            copier copy --trust --vcs-ref ${version} \
            "${copier_arguments[@]}" \
            "${template}" "${repository_name}" "${@}"
    else
        echo "Using local template: ${template}"
        uvx --python "${python_binary}" \
            --with copier-template-extensions --with pycountry \
            copier copy --trust \
            "${copier_arguments[@]}" \
            "${template}" "${repository_name}" "${@}"
    fi
}

parse_arguments "$@"
echo "Creating repository '${repository_name}' using template '${template}' with version '${version}'..."
create_repository


echo "Generating certificates"
openssl req -x509 -newkey rsa:4096 -nodes \
    -out ${repository_name}/docker/development.crt \
    -keyout ${repository_name}/docker/development.key \
    -days 3650 -subj "/C=CH/ST=./L=./O=./OU=./CN=localhost/emailAddress=."

echo "Removing previous containers"
(
    cd "${repository_name}"/docker
    ln -s ../variables .env
    docker compose down || true
    rm .env
)