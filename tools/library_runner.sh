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

set -euo pipefail

# Source common functions (echo, linting, formatting, etc.)
# When in the source repo: common.sh is next to this file.
# When deployed: .runner-common.sh is next to .runner.sh.
_runner_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${_runner_dir}/common.sh" ]; then
    # shellcheck disable=SC1091
    source "${_runner_dir}/common.sh"
elif [ -f "${_runner_dir}/.runner-common.sh" ]; then
    # shellcheck disable=SC1091
    source "${_runner_dir}/.runner-common.sh"
else
    echo "Downloading .runner-common.sh from oarepo repository..." >&2
    curl --fail -o "${_runner_dir}/.runner-common.sh" \
        https://raw.githubusercontent.com/oarepo/oarepo/main/tools/common.sh
    chmod +x "${_runner_dir}/.runner-common.sh"
    # shellcheck disable=SC1091
    source "${_runner_dir}/.runner-common.sh"
fi
unset _runner_dir

# needed for osx to get DYLD_LIBRARY_PATH working
if [ -f ~/.envrc.local ] ; then
    # shellcheck disable=SC1090
    source ~/.envrc.local
fi

# region: Initial setup
export UV_EXTRA_INDEX_URL=${UV_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL:-"https://gitlab.cesnet.cz/api/v4/projects/1408/packages/pypi/simple"}
export INVENIO_APP_THEME='["semantic-ui"]'
export INVENIO_WEBPACKEXT_NPM_PKG_CLS="pynpm.package:PNPMPackage"
export INVENIO_JAVASCRIPT_PACKAGES_MANAGER="pnpm"
export INVENIO_ASSETS_BUILDER="rspack"
export INVENIO_THEME_FRONTPAGE="False"
export INVENIO_THEME_CSS_TEMPLATE="oarepo_ui/css.html"
export FLASK_DEBUG=1
export LC_TIME=${LC_TIME:-"en_US.UTF-8"}

cd "$(dirname "$0")"

if [ ! -f pyproject.toml ]; then
    echo "No pyproject.toml found, please migrate from setup.cfg."  >&2
    echo "See https://github.com/oarepo/oarepo/blob/main/README.md for details."  >&2
    exit 1
fi

if [ -f setup.cfg ]; then
    echo "setup.cfg found, please migrate to pyproject.toml."  >&2
    echo "See https://github.com/oarepo/oarepo/blob/main/README.md for details."  >&2
    exit 1
fi

package_name=$(get_package_name)

export package_name

# Detect code directories (exclude tests for jslint)
if [ "${1:-''}" = "jslint" ]; then
    detect_code_directories false
else
    detect_code_directories true
fi
# endregion: Initial setup

# region: Main command dispatcher and help output
run_tools() {
    set -e
    set -o pipefail

    # Parse the commandline according to the options defined above.

    FIRST_OAREPO_VERSION=$(first_oarepo_version)
    export FIRST_OAREPO_VERSION
    export OAREPO_VERSION=${OAREPO_VERSION:-${FIRST_OAREPO_VERSION}}
    export NO_EDITABLE=${NO_EDITABLE:-""}
    export SKIP_SERVICES=${SKIP_SERVICES:-""}
    export WITH_COVERAGE=${WITH_COVERAGE:-""}

    while [[ $# -gt 0 ]]; do
        case $1 in
            venv)
                shift
                setup_venv --force "$@"
                return 0
                ;;
            upgrade)
                upgrade_environment
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
                uvx --from oarepo-tools make-translations "$@"
                return 0
                ;;
            lint)
                shift
                setup_venv
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
            jstest)
                shift
                run_jstest "$@"
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
                echo "Unknown command: $1"  >&2
                show_help
                exit 1
                ;;
        esac
    done
    show_help
    return 0
}

show_help() {
    (
    echo "Usage: $0 [options] [command]"
    echo ""
    echo "Commands:"
    echo "  venv              Set up the virtual environment"
    echo "      --no-editable     Do not install the package in editable mode, build it first"
    echo "      --force           Force the creation of the virtual environment, removing any existing one"
    echo "  upgrade           Upgrade the environment (clean cache and recreate venv)"
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
    echo "  OAREPO_VERSION    The version of OARepo to use (default: first oarepoXY in pyproject.toml)"
    echo "  PYTHON            The Python executable to use (default: highest version from oarepo-versions available on system)"
    echo ""
    echo "Housekeeping commands:"
    echo "  self-update       Update the runner script"
    ) >&2
    return 0
}

first_oarepo_version() {
    grep -E '^oarepo[0-9][0-9]\s*=' pyproject.toml | head -n1 | sed 's/oarepo//' | sed 's/\s*=.*//'
}
# endregion: Main command dispatcher and help output

# region: Version commands
list_oarepo_versions() {
    # if there is a pyproject.toml, get its dependencies section and parse the
    # "oarepo[rdm,tests]>=13.0.0,<15.0.0" line to get the version of oarepo.
    # return 13,14 in this case
    if [ -f pyproject.toml ]; then
        echo -n "{"
        echo -n "\"oarepo_versions\": "
        get_oarepo_versions
        echo -n ", "
        echo -n "\"python_versions\": "
        get_python_versions "$(get_oarepo_versions)"
        echo -n ", "
        echo -n "\"node_versions\": [\"24\"]"
        echo "}"
    else
        echo "No pyproject.toml found and other types are not supported yet." >&2
        echo "Please ensure you are in the correct directory." >&2
        exit 1
    fi
}

get_oarepo_versions()
{
    versions=$(grep -E "^oarepo[0-9]{2}\s*=" pyproject.toml | sed "s/oarepo\([0-9][0-9]\)\s*=.*/\"\1\"/" | sort -n |tr '\n' ',' | sed 's/,$//')
    echo -n "[$versions]"
}


get_python_versions() {
    local oarepo_versions
    local -a python_versions
    oarepo_versions="$1"
    python_versions=()
    if [[ "$oarepo_versions" == *"14"* ]]; then
        python_versions+=("\"3.14\"")
    else
        echo "Unknown oarepo version(s) $oarepo_versions, cannot determine python versions." >&2
        exit 1
    fi
    local python_versions_str
    python_versions_str=$(IFS=,; echo "${python_versions[*]}")
    # return concatenated string of python versions as json array of strings
    echo -n "[$python_versions_str]"
}
# endregion: Version commands

# region: Services management
# Test services (start_test_services, stop_test_services) are provided by common.sh.
# Keep these wrappers for backward compatibility with other functions that use them.
stop_services() {
    if [ -n "$SKIP_SERVICES" ]; then
        return 0
    fi
    stop_test_services
}

start_services() {
    if [ -n "$SKIP_SERVICES" ]; then
        return 0
    fi
    start_test_services
}
# endregion: Services management

# region: Python Virtual Environment Management

get_highest_available_python() {
    # Get python versions from oarepo-versions
    local python_versions
    python_versions=$(list_oarepo_versions | grep -o '"python_versions":[^]]*]' | sed 's/"python_versions"://' | sed 's/[][]//g' | sed 's/"//g' | tr ',' ' ')

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

    if [ -z "$highest_version" ]; then
        echo "No compatible Python version found on the system." >&2
        echo "Available versions according to oarepo-versions: $python_versions" >&2
        exit 1
    fi

    echo "$highest_version"
}

setup_venv() {
    set -e
    set -o pipefail

    FORCE=${FORCE:-0}

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
                echo "Unknown venv option: $1" >&2
                exit 1
                ;;
        esac
    done


    if [ "$FORCE" = "1" ] && [ -d .venv ]; then
        echo "Removing existing virtual environment..." >&2
        rm -rf .venv
    fi

    if [ -d .venv ] ; then
        return 0
    fi

    # If PYTHON is set, use it directly. Otherwise, find the highest available version.
    if [ -z "${PYTHON:-}" ]; then
        PYTHON_VERSION=$(get_highest_available_python)
        export PYTHON_VERSION
        export PYTHON="python${PYTHON_VERSION}"
    fi

    echo "Setting up virtual environment with Python $PYTHON and oarepo version $OAREPO_VERSION"  >&2
    uv venv --python="$PYTHON" --seed
    source .venv/bin/activate

    uv pip install setuptools
    uv pip install --prerelease allow "oarepo[rdm,tests]>=${OAREPO_VERSION},<$((OAREPO_VERSION + 1))"

    default_extras=$(grep '^default_extras' pyproject.toml | awk -F'"' '{print $2}' || true)

    if [ -z "$NO_EDITABLE" ]; then
        echo "Installing the package in editable mode."  >&2
        uv pip install --prerelease allow -e ".[dev,tests,oarepo${OAREPO_VERSION}${default_extras:+,${default_extras}}]" || uv pip install --prerelease allow -e ".[dev,tests,oarepo${OAREPO_VERSION}${default_extras:+,${default_extras}}]"
    else
        echo "Building and Installing the package."  >&2
        if [ -d dist ]; then
            echo "Removing existing dist directory..."  >&2
            rm -rf dist
        fi
        uv build --wheel || uv build --wheel
        wheel_package=$(ls dist/*.whl | head -n 1)
        uv pip install --prerelease allow "${wheel_package}[tests,oarepo${OAREPO_VERSION}${default_extras:+,${default_extras}}]" || uv pip install --prerelease allow "${wheel_package}[tests,oarepo${OAREPO_VERSION}${default_extras:+,${default_extras}}]"
    fi
}

upgrade_environment() {
    set -e
    set -o pipefail

    echo "Upgrading environment..."  >&2

    # Stop services if running
    echo "Stopping services..."  >&2
    stop_services || true

    # Remove .venv if it exists
    if [ -d .venv ]; then
        echo "Removing virtual environment..."  >&2
        rm -rf .venv
    fi

    # Clean uv cache
    echo "Cleaning uv cache..."  >&2
    uv cache clean

    # Recreate virtual environment
    echo "Setting up virtual environment..."  >&2
    setup_venv --force

    echo "Upgrade completed successfully."  >&2
}
# endregion: Python Virtual Environment Management

# region: Run commands in the virtual environment (invenio, cli, with services, ...)
run_command() {
    set -e
    set -o pipefail

    local command_name="$1"
    shift

    local non_processed_args=()

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
    if [ -z "${SKIP_SERVICES:-}" ]; then
        start_services
    fi

    source .venv/bin/activate
    source .env-services
    "$command_name" "${non_processed_args[@]}"
}

# shellcheck disable=SC2120
in_invenio_shell() {
    set -e
    set -o pipefail

    local cmd
    export PYTHON_BASIC_REPL=0
    if [ -t 0 ]; then
        # stdin is a terminal, so take args instead
        cmd="$*"
    else
        cmd=$(cat)
    fi

    run_command invenio shell --no-term-title ${SKIP_SERVICES:+--skip-services} -c "${cmd}"
}

# endregion: Run commands in the virtual environment (invenio, cli, with services, ...)

# region: Python and javascript tests

run_tests() {
    set -euo pipefail

    local test_args=()
    local skip_services=0
    local with_coverage=0

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-services)
                skip_services=1
                shift
                ;;
            --with-coverage)
                with_coverage=1
                shift
                ;;
            *)
                test_args+=("$1")
                shift
                ;;
        esac
    done

    setup_venv

    if [ -f ./test-setup.sh ]; then
        echo_progress "Sourcing test setup script..."
        source ./test-setup.sh
    fi

    # unset all INVENIO_ environment variables to avoid interference with tests
    unset $(env | grep ^INVENIO_ | sed 's/=.*//') 2>/dev/null || true

    if [ "$skip_services" -eq 0 ]; then
        start_test_services
    fi

    if [ "$with_coverage" -eq 1 ]; then
        setup_test_coverage
    fi

    source .venv/bin/activate
    pytest "${test_args[@]}"

    if [ "$skip_services" -eq 0 ]; then
        stop_test_services
    fi
}

setup_jstests() {
    set -e
    set -o pipefail

    local instance_path assets_path package_root webpack_entries coverage_roots test_roots rdm_dev_dependencies

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-services)
                SKIP_SERVICES=1
                shift
                ;;
            --with-storybook)
                WITH_STORYBOOK=1
                shift
                ;;
            *)
                echo "Unknown setup tests option: $1"  >&2
                exit 1
                ;;
        esac
    done

    instance_path=$(echo "print(app.instance_path, end='')" | in_invenio_shell | tail -n1)
    assets_path="${instance_path}/assets"
    package_root="${PWD}"

    run_command invenio ${SKIP_SERVICES:+--skip-services} webpack clean create

    # Needed to work around Invenio RSPack error:
    #  ERROR: packages field missing or empty
    in_invenio_shell <<EOF
import yaml
from pathlib import Path
workspace_file = Path("${assets_path}") / "pnpm-workspace.yaml"
with workspace_file.open("r") as f:
    workspace = yaml.safe_load(f) or {}

workspace.setdefault("packages", [])

with workspace_file.open("w") as f:
    yaml.safe_dump(workspace, f, sort_keys=False)
EOF

    ensure_npm_script test 'jest $@'

    webpack_entries=$(get_webpack_entries)
    coverage_roots=$(echo "$webpack_entries" | tr ',' '\n' | sed 's|$|/**/*.{js,jsx}|' | sed 's/^\./"**/; s/$/"/' | paste -sd, -)
    test_roots=$(echo "$webpack_entries" | tr ',' '\n' | xargs -I{} realpath "${assets_path}/{}" | sed 's/^/"/; s/$/"/' | paste -sd, -)

    cat <<EOF >"${assets_path}/jest.config.js"
/**
 * For a detailed explanation regarding each configuration property, visit:
 * https://jestjs.io/docs/configuration
 */

const fs = require("fs");
const webpackConfig = require("./build/config.json");

/** @type {import('jest').Config} */
const config = {
  clearMocks: true,
  collectCoverageFrom: [
    ${coverage_roots},
    "!**/node_modules/**",
  ],
  coverageDirectory: "_coverage",
  coverageProvider: "v8",
  moduleDirectories: ["${assets_path}/node_modules"],
  moduleFileExtensions: ["js", "jsx", "json"],
  moduleNameMapper: {
    ...Object.fromEntries(
      Object.entries(webpackConfig.aliases).map(([alias, path]) => {
        const escapedAlias = alias.replace(/[.*+?^\${}()|[\]\\\]/g, "\\\\$&");
        try {
          const realPath = fs.realpathSync(path)
          return [\`^\${escapedAlias}(.*)\$\`, \`\${realPath}\$1\`];
        } catch {
          return [\`^\${escapedAlias}(.*)\$\`, \`<rootDir>/\${path}\$1\`]
        }
      })),
    '^axios$': require.resolve('axios'),
  },
  rootDir: "${package_root}",
  roots: [${test_roots}],
  testEnvironment: "jsdom",
  setupFilesAfterEnv: [
    '${assets_path}/setupTests.js',
  ],
  transform: {
    "^.+\\.(js|jsx)\$": [
      'babel-jest', {
      presets: [
        ['@babel/preset-env', {
          targets: { chrome: '48' },
          modules: 'auto'
        }],
        '@babel/preset-react'
      ],
      plugins: [
        '@babel/plugin-transform-modules-commonjs',
        '@babel/plugin-transform-runtime'
      ]
    }]
  },
  // Environment variables simulation
  globals: {
    'process.env': {
      NODE_ENV: 'test',
      ...process.env  // Preserve existing environment variables
    }
  },
  transformIgnorePatterns: [
    "node_modules/(?!axios|react-error-boundary|sanitize-html)",
  ],
};

module.exports = config;
EOF

    cat <<'EOF' >"${assets_path}/setupTests.js"
// This file is part of Invenio-RDM-Records
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});
EOF
    # Collect statics & install rspack project dependencies
    run_command invenio --skip-services collect
    run_command invenio --skip-services webpack install

    # Fetch & install testing devDeps from invenio-rdm-records (Jest & friends)
    rdm_dev_dependencies=$(in_invenio_shell <<EOF
import json
import pathlib
import invenio_rdm_records

package_json_path = (
    pathlib.Path(invenio_rdm_records.__file__).parent
    / "assets/semantic-ui/js/invenio_rdm_records/package.json"
)

with package_json_path.open("r") as f:
    package_json = json.load(f)

dev_deps = package_json.get("devDependencies", {})

print(" ".join(f"{name}@{version}" for name, version in dev_deps.items()))
EOF
    )

    # shellcheck disable=SC2086
    pnpm add -C "$assets_path" -w -D $rdm_dev_dependencies

    if [ -n "${WITH_STORYBOOK:-}" ]; then
        setup_storybook
    fi
}

setup_storybook() {
    local instance_path assets_path package_root webpack_entries story_paths
    instance_path=$(echo "print(app.instance_path, end='')" | in_invenio_shell | tail -n1)
    assets_path="${instance_path}/assets"
    package_root="${PWD}"

    pnpm add -C "${assets_path}" -w -D @storybook/addon-docs@^9.1.2 @storybook/addon-webpack5-compiler-swc@^3.0.0 @storybook/react-webpack5@^9.1.2 storybook@^9.1.2 @storybook/test@^8.6.14


    ensure_npm_script "storybook" "storybook dev -p 6006"
    ensure_npm_script "build-storybook" "storybook build"

    if [ ! -d  "${assets_path}/.storybook" ]; then
        mkdir -p "${assets_path}/.storybook"
    fi

    webpack_entries=$(get_webpack_entries)
    story_paths=$(echo "$webpack_entries" | tr ',' '\n' | sed 's|$|/**/*.stories.@\(js\|jsx\)|' | sed 's/^\./"../; s/$/"/' | paste -sd, -)

    cat <<EOF > "${assets_path}/.storybook/main.js"
import path from "path"

/** @type { import('@storybook/react-webpack5').StorybookConfig } */
const config = {
  stories: [
    ${story_paths}
  ],
  addons: [
    "@storybook/addon-webpack5-compiler-swc",
    "@storybook/addon-docs"
  ],
  core: {
    "disableTelemetry": true,
  },
  webpackFinal: async (config) => {
    // Always resolve symlinked imports against local node_modules
    config.resolve.modules = [
      path.resolve(__dirname, "../node_modules"),
      "node_modules",
    ];
    config.resolve.symlinks = false;
    return config;
  },
  staticDirs: [
    { from: "../../static/", to: "/static/" }
  ],
  framework: {
    "name": "@storybook/react-webpack5",
    "options": {}
  }
};
export default config;
EOF

    cat <<EOF > "${assets_path}/.storybook/preview.js"
import 'semantic-ui-css/semantic.min.css';

/** @type { import('@storybook/react-webpack5').Preview } */
const preview = {
  parameters: {
    autodocs: true,
    controls: {
      matchers: {
       color: /(background|color)$/i,
       date: /Date$/i,
      },
    },
  },
};

export default preview;
EOF

    cat <<EOF >.invenio
[cli]
flavour = RDM
EOF

    cat <<EOF >.invenio.private
[cli]
services_setup = True
instance_path = ${instance_path}
EOF
    # TODO: update nrp-cli to use correct config-file
    run_invenio_cli less register --theme-config-file "${assets_path}/less/theme.config"
    run_command invenio webpack build

    in_invenio_shell <<EOF
from flask import render_template
from bs4 import BeautifulSoup

with app.test_request_context("/", method="GET"):
    html = render_template("oarepo_ui/base_page.html", embedded=True)

soup = BeautifulSoup(html, "html.parser")

head_content = soup.head.decode_contents().strip()
body_content = soup.body.decode_contents().strip()

with open("${assets_path}/.storybook/preview-head.html", "w", encoding="utf-8") as f:
    f.write(head_content)

with open("${assets_path}/.storybook/preview-body.html", "w", encoding="utf-8") as f:
    f.write(body_content)
EOF
}

run_jstest() {
    set -e
    set -o pipefail

    local non_processed_args=()

    while [[ $# -gt 0 ]]; do
        if [ "$1" = "setup" ]; then
          shift
          setup_jstests "$@"
          return 0
        fi
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


    run_command invenio ${SKIP_SERVICES:+--skip-services} webpack run test "${non_processed_args[@]}"
    return 0
}

get_webpack_entries() {
    set -eo pipefail

    local webpack_entries
    # Figure out asset paths for entries in .venv
    webpack_entries=$(in_invenio_shell <<EOF
import os
import importlib_metadata

dist = importlib_metadata.distribution("${package_name}")

def flatten(v):
    if isinstance(v, str): return [v]
    if isinstance(v, (list, tuple, set)):
        return [p for x in v for p in flatten(x)]
    return []

entries = [
    e
    for ep in dist.entry_points if ep.group == "invenio_assets.webpack"
    for v in ep.load().entry.values()
    for e in flatten(v)
]

common_roots = {
    os.path.dirname(path)
    for path in entries
    if not any(
        path != other and path.startswith(other.rstrip("/") + "/")
        for other in entries
    )
}

roots_list = sorted([root for root in common_roots if root])
print(",".join(roots_list))
EOF
    )
    echo -n "$webpack_entries"
}

ensure_npm_script() {
    local instance_path assets_path package_root script_name script_index
    instance_path=$(echo "print(app.instance_path, end='')" | in_invenio_shell | tail -n1)
    assets_path="${instance_path}/assets"
    package_root="${PWD}"

    script_name="$1"
    shift

    script_index=$(pnpm -C "${assets_path}" -c exec "jq -r '(.scripts | keys | index(\"${script_name}\"))' package.json")

    if [ "${script_index}" == "null" ]; then
        # Ensure script is defined in package.json
        in_invenio_shell <<EOF
import json
from pathlib import Path

package_file = Path("${assets_path}") / "package.json"

with package_file.open("r") as f:
    package_data = json.load(f)

scripts = package_data.setdefault("scripts", {})
scripts["${script_name}"] = '$@'

with package_file.open("w") as f:
    json.dump(package_data, f, indent=2)
EOF
    fi
}
# endregion: Python and javascript tests


# region: Housekeeping
cleanup() {
    set -e
    set -o pipefail

    echo "Stopping services..."  >&2
    stop_services

    if [ -d .venv ]; then
        echo "Removing virtual environment..."  >&2
        rm -rf .venv
    fi

    if [ -f .env-services ]; then
        echo "Removing environment file..."  >&2
        rm -f .env-services
    fi

    echo "Cleanup completed."  >&2
}

self_update() {
    set -euo pipefail

    echo "Updating runner script..."  >&2
    curl --fail -o "./.runner-new.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/library_runner.sh
    chmod +x "./.runner-new.sh"
    if "./.runner-new.sh" check-script-working ; then
        mv "./.runner-new.sh" "./.runner.sh"
        self_update_common
        echo "Runner script updated successfully."  >&2
    else
        echo "New runner script is not working, keeping the old one."  >&2
        rm "./.runner-new.sh"
    fi
    return 0
}
# endregion: Housekeeping


# run the tools and exit to prevent evaluation after this line in case the script
# is self updated
run_tools "$@"; exit;
