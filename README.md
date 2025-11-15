# OARepo flavour of Invenio RDM repository

## Introduction

This repository contains a meta-package `oarepo` that bundles together
all the necessary dependencies for the OARepo flavour of Invenio RDM repository.

This flavour is used in the Czech National Repository Platform project
and the Czech National Repository.

By installing the `oarepo[rdm,tests]` package, you will get all the
Invenio RDM dependencies that are thoroughly tested when the package is
being released. These dependencies will contain the patches that are
needed to support advanced scenarios, such as multiple models and
deposition workflows.

To use the RDM12 version, install `oarepo[rdm,tests]>=12,<13`. To get
the dependencies for v13, install `oarepo[rdm,tests]>=13,<14`.

**Note:** Always pin the `oarepo` package to a range of versions as the provided
tools parse this information to determine how to set up the package and test it.

## Layout of this repository

The main trunk of the repository is used for development tools, does not contain
the RDM packages. For these, there are separate branches
[`rdm-12`](https://github.com/oarepo/oarepo/tree/rdm-12),
[`rdm-13`](https://github.com/oarepo/oarepo/tree/rdm-13) and
[`rdm-14`](https://github.com/oarepo/oarepo/tree/rdm-14).
Please visit these branches to see the actual packages and their dependencies.

## Tools

The main trunk of the repository contains a set of tools that can be used
in the development of oarepo-based libraries and repositories. These include
both command-line tools and reusable GitHub actions.

### Command-line tools

The command-line tools are put into your library when the library is created, see below.
To run the tools, just run the `run.sh` script in the root of your repository.

This script will automatically download the latest version of the `.runner.sh` script
from the oarepo repository and execute it with the arguments passed to the
script. If no arguments are passed, it will run the default command `test`.

Available commands and options are:

```text
Usage: .runner.sh [options] [command]

Commands:
  venv              Set up the virtual environment
  start             Start the docker services for testing
  stop              Stop the docker services after testing
  test              Run the tests
  oarepo-versions   List the supported OARepo versions for
                    this package
  clean             Clean up the environment
                    (stop services, remove venv, etc.)
  shell             Start a shell with the virtual environment
                    and services running
  invenio           Run an Invenio command with the virtual environment
                    and services running
  translations      Run the make-translations command

Environment variables:
  OAREPO_VERSION    The version of OARepo to use (default: 13)
  PYTHON_VERSION    The Python interpreter to use (default: 3.13)
  PYTHON            The Python executable to use (default: python3.13)
```

To use the command-line tools, please create a `run.sh` script inside
your GitHub repository with the following content:

```bash
#!/usr/bin/env bash
#
# This script sets up a Python virtual environment, installs necessary packages,
# runs tests and other tasks for libraries which are part of the OARepo Invenio RDM
# flavour.
# 
# Usage: ./run.sh --help
#
#
# (C) 2025 CESNET, z.s.p.o.
# OARepo is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#
set -euo pipefail

base_dir="$(dirname "$0")"

if [ ! -f "${base_dir}/.runner.sh" ]; then
  echo "Downloading .runner.sh from oarepo repository..." >&2
  curl -o "${base_dir}/.runner.sh" https://raw.githubusercontent.com/oarepo/oarepo/main/tools/library_runner.sh
  chmod +x "${base_dir}/.runner.sh"
fi

"${base_dir}/.runner.sh" "$@"
```

## GitHub Workflows

The library is configured to use the reusable GitHub workflows from this repository.
These workflows are used to build, test, and release the library and are automatically
updated.

## Setting up a new library

### Secrets

Set up the following secrets in your repository (for the oarepo organization, these are set up automatically):

* `OAREPO_BUMP_VERSION_CLIENT_ID`
* `OAREPO_BUMP_VERSION_CLIENT_PASSWORD`
* `PYPI_PASSWORD`
* `NPM_PASSWORD`

### Initial files

Copy the content of the `library` directory from the main trunk of this repository to the root of your repository. Make sure you have the following directories/files:

* `.github` containing the workflows
* `.gitignore` file
* `run.sh` script

Push these changes to the main branch of your repository before proceeding.

### Ruleset for main branch

The main branch should be protected from direct modifications.
To set it up, go to the GitHub settings of your repository, click on
"Rules/Rulesets" and create a new ruleset for the main branch:

* Ruleset name: `locked main`
* Bypass list: `OARepoVersionBump`
* Target branches: `default`
* Restrict deletions
* Require linear history
* Require pull request before merging
  * Require approvals: `1`
  * Dismiss stale pull request approvals when new commits are pushed
  * Require approval of the most recent reviewable push
  * Automatically request Copilot code review
  * Allow merge methods: `rebase`
* Block force pushes
* Require status checks to pass before merging
  * CodeQL: `High or higher`, Alert: `Errors`

### Testing

* Make some changes to the code and try to push them to the main branch - this should fail
* Create a new branch and push it
* Verify that GitHub actions are triggered and that the tests are run
* Create a pull request to the main branch
* Verify that Copilot and CodeQL checks have been called
* Verify that the pull request is ready to be merged
* Merge the PR and wait until the tests in the main branch pass

### Releasing a new version

To release a new version of your library, go to the Releases sidebar of
your GitHub repository and draft a release there. After publishing the release,
the version file inside the release branch (normally main) will be
updated with the version number specified in the release, and the release
should be propagated to pypi.org.

## Migrating an existing library

To migrate an existing library to use the OARepo tools, follow these steps:

1. Backup your existing library
2. Remove the `.github/` folder and `run-tests.sh`, `.gitignore` files (copy existing ignored paths if needed)
3. Copy the content of the `library` directory from the main trunk of this repository to the root of your repository.
4. If there is a setup.py/setup.cfg file
    1. if there also is a pyproject.toml file containing just the buildsystem declaration,
       remove the toml file
    2. run `uvx hatch new --init` to create a new pyproject.toml file
    3. check that the file contains the correct dependencies and entry points and modify it if necessary
    4. if the library did not store the version in the `__init__.py` file, add the actual
       version string to that file. See [invenio example](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/__init__.py) on how to do that.
    5. run the `uvx hatch build` command to build the package and correct any errors (for example, set license type to MIT)
    6. remove the `setup.py` and `setup.cfg` files
    7. make sure that the library contains the `oarepo` dependency in the `pyproject.toml` file
       (e.g. `oarepo[rdm,tests]>=13,<14`)
    8. add mypy &  pytest configuration to the `pyproject.toml` file, for example:

    ```toml
        [tool.pytest.ini_options]
        testpaths = [
            "tests",
            "src"
        ]
    ```

5. run the `run.sh clean` command to remove the old virtual environment and other files
6. run the `run.sh test` command to check that the library is working correctly after the migration
7. run the `run.sh lint` command and fix any issues reported by the linter
8. set the secrets in your repository as described above
9. set up the ruleset for the main branch as described above
10. commit the changes to a branch and create a pull request to the main branch
