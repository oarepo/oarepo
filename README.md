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
[`rdm-12`](https://github.com/oarepo/oarepo/tree/rdm-12) and
[`rdm-13`](https://github.com/oarepo/oarepo/tree/rdm-13).
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