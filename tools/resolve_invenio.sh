#!/usr/bin/env bash
# resolve_invenio.sh
#
# Scans Python sources for invenio-* / pytest-invenio imports, looks up the
# installed version in the local .venv, and prints pyproject.toml-ready
# version constraints to stdout.
#
# Packages that are already transitive dependencies of another package in the
# result set are pruned, so the output contains only the true top-level roots.
#
# Requires: bash >= 4.x (e.g. the Homebrew bash on macOS), uv in PATH
#
# Usage:
#   ./resolve_invenio.sh <source-dir> [<source-dir> ...]
#
# Environment:
#   VENV_DIR   path to the virtual environment  (default: .venv)

set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"

# ── logging ────────────────────────────────────────────────────────────────────
# All messages go to stderr so that stdout carries only the final constraints.

info() { printf '\033[0;34m[info]\033[0m  %s\n'  "$*" >&2; }
warn() { printf '\033[0;33m[warn]\033[0m  %s\n'  "$*" >&2; }
die()  { printf '\033[0;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

# ── uv wrapper ────────────────────────────────────────────────────────────────

# _uv_pip <subcommand> [args...]
# Runs `uv pip` against VENV_DIR by injecting VIRTUAL_ENV, which uv respects
# the same way pip does – no need to pass --python on every call.
_uv_pip() {
    VIRTUAL_ENV="${VENV_DIR}" uv pip "$@"
}

# ── step 1: find Python source files ──────────────────────────────────────────

# find_python_sources <dir> [<dir>...]
# Emits sorted paths of every *.py file under the given directories.
find_python_sources() {
    find "$@" -type f -name '*.py' | sort
}

# ── step 2: extract top-level invenio module names ────────────────────────────

# extract_invenio_modules <file> [<file>...]
# Parses import statements and emits unique top-level module names for any
# package in the invenio-* / pytest-invenio family.
#
# Handles all standard import forms:
#   import invenio_records
#   import invenio_records.api
#   from invenio_records import Record
#   from invenio_records.api import Record
#   from pytest_invenio.fixtures import ...
#
# Emits names like:  invenio_records_resources  pytest_invenio
extract_invenio_modules() {
    grep -hE '^\s*(import|from)\s+(invenio[a-zA-Z0-9_]*|pytest_invenio)' \
            "$@" 2>/dev/null \
        | sed -E \
            -e 's/^\s*(import|from)\s+//' \
            -e 's/[.([:space:]].*//'       \
        | grep -E '^(invenio|pytest_invenio)' \
        | sort -u \
    || true   # grep exits 1 on no match; that is not an error here
}

# ── step 3: map Python module name → pip package name ─────────────────────────

# module_to_package <module>
# Replaces underscores with dashes (Python import convention → PyPI convention).
#   invenio_records_resources  ➜  invenio-records-resources
#   pytest_invenio             ➜  pytest-invenio
module_to_package() {
    printf '%s' "${1//_/-}"
}

# ── step 4: version lookup ────────────────────────────────────────────────────

# get_installed_version <package>
# Prints the version string reported by `uv pip show`, or nothing if absent.
get_installed_version() {
    local package="$1"
    _uv_pip show "$package" 2>/dev/null \
        | awk '/^Version:/ { print $2 }' \
    || true
}

# ── step 5: dependency pruning ────────────────────────────────────────────────

# get_invenio_tree_deps <package>
# Uses `uv pip tree` to emit the names of every invenio-* / pytest-invenio
# package that <package> transitively depends on (the root itself included).
# This delegates the full resolution to uv rather than reimplementing it.
get_invenio_tree_deps() {
    local package="$1"
    _uv_pip tree --package "$package" 2>/dev/null \
        | grep invenio          \
        | sed 's/^[^a-z]*//'   \
        | sed 's/ .*//'         \
        | sort -u               \
    || true
}

# prune_transitive_deps <package> [<package>...]
# Removes every package from the list that already appears in the transitive
# dependency tree of another package in the same list.
#
# Algorithm:
#   For each package P, fetch its full invenio subtree via `uv pip tree`.
#   Any other package Q in our list that shows up in P's subtree is covered
#   by P and therefore redundant.  Only the uncovered roots are emitted.
prune_transitive_deps() {
    local -a pkgs=("$@")

    # Build a set for O(1) membership tests
    declare -A in_list=()
    for pkg in "${pkgs[@]}"; do
        in_list["$pkg"]=1
    done

    # Discover which packages are covered (transitively depended on) by others
    declare -A covered_by=()
    for pkg in "${pkgs[@]}"; do
        local -a tree_deps=()
        mapfile -t tree_deps < <(get_invenio_tree_deps "$pkg")

        for dep in "${tree_deps[@]}"; do
            [[ "$dep" == "$pkg" ]] && continue          # skip self
            [[ ! -v in_list["$dep"] ]]  && continue     # not in our list
            [[ -v covered_by["$dep"] ]] && continue     # already recorded
            covered_by["$dep"]="$pkg"
        done
    done

    # Emit surviving roots; log every pruned package with its covering parent
    local -a result=()
    for pkg in "${pkgs[@]}"; do
        if [[ -v covered_by["$pkg"] ]]; then
            info "  Pruning ${pkg}  (transitive dep of ${covered_by[$pkg]})"
        else
            result+=("$pkg")
        fi
    done

    if [[ ${#result[@]} -gt 0 ]]; then
        printf '%s\n' "${result[@]}"
    fi
}

# ── step 6: format a pyproject.toml-compatible constraint ─────────────────────

# format_constraint <package> <version>
# Prints:  "package>=major.0.0,<(major+1).0.0",
format_constraint() {
    local package="$1"
    local version="$2"
    local major="${version%%.*}"          # pure-bash, no subprocess
    printf '"%s>=%s.0.0,<%d.0.0",\n' "$package" "$major" "$((major + 1))"
}

# ── main ───────────────────────────────────────────────────────────────────────

main() {
    [[ $# -gt 0 ]] || die "Usage: $(basename "$0") <source-dir> [<source-dir>...]"

    local dirs=("$@")

    # Validate source directories
    for d in "${dirs[@]}"; do
        [[ -d "$d" ]] || die "Not a directory: $d"
    done

    # Validate tooling
    command -v uv > /dev/null 2>&1 \
        || die "uv not found in PATH"
    [[ -x "${VENV_DIR}/bin/python" ]] \
        || die "Python not found at '${VENV_DIR}/bin/python' – set VENV_DIR or run from the project root."

    info "Virtual env         : ${VENV_DIR}"
    info "Scanning directories: ${dirs[*]}"

    # ── 1. Collect Python source files ────────────────────────────────────────
    local -a py_files
    mapfile -t py_files < <(find_python_sources "${dirs[@]}")

    info "Python source files : ${#py_files[@]}"
    [[ ${#py_files[@]} -gt 0 ]] || { warn "No Python files found."; return 0; }

    # ── 2. Extract unique invenio module names → normalised package names ─────
    local -a modules
    mapfile -t modules < <(extract_invenio_modules "${py_files[@]}")

    info "Unique invenio modules: ${#modules[@]}"
    [[ ${#modules[@]} -gt 0 ]] || { warn "No invenio imports found."; return 0; }

    local -a packages=()
    for module in "${modules[@]}"; do
        packages+=("$(module_to_package "$module")")
    done

    # ── 3. Prune packages already covered by another package's transitive deps ─
    info "Pruning transitive dependencies..."

    local -a top_packages=()
    mapfile -t top_packages < <(prune_transitive_deps "${packages[@]}")

    info "Packages after pruning: ${#top_packages[@]}"
    [[ ${#top_packages[@]} -gt 0 ]] || { warn "All packages were pruned – this is unexpected."; return 0; }

    # ── 4. Resolve versions and collect constraints ───────────────────────────
    local -a constraints=()

    for package in "${top_packages[@]}"; do
        local version
        version=$(get_installed_version "$package")

        if [[ -z "$version" ]]; then
            warn "  ${package}  – not installed in ${VENV_DIR}, skipping"
            continue
        fi

        info "  ${package}==${version}"
        constraints+=("$(format_constraint "$package" "$version")")
    done

    info "Done – ${#constraints[@]} constraint(s) follow."
    [[ ${#constraints[@]} -gt 0 ]] || { warn "No constraints could be resolved – verify your venv."; return 0; }

    # ── 5. Emit all constraints to stdout at once ─────────────────────────────
    printf '%s\n' "${constraints[@]}"
}

main "$@"
