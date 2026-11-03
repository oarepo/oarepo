#!/usr/bin/env python3

"""Run pybabel using options from pyproject.toml's [tool.babel.*] tables.

Replacement for the old ``python setup.py compile_catalog`` (and friends).
Only stdlib is needed to run this script; Babel itself is taken from the
current interpreter, a ``pybabel`` on PATH, or ``uvx --from babel``.

Usage:
    babel_catalog.py [compile|extract|init|update] [--project DIR] [--dry-run] [-- extra pybabel args]

Examples:
    babel_catalog.py                      # compile, using [tool.babel.compile_catalog]
    babel_catalog.py extract -- invenio_app_rdm
    babel_catalog.py init -- -l cs
"""

import argparse
import importlib.util
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

SECTIONS = {
    "compile": "compile_catalog",
    "extract": "extract_messages",
    "init": "init_catalog",
    "update": "update_catalog",
}


def pybabel_cmd() -> list[str]:
    if importlib.util.find_spec("babel"):
        return [sys.executable, "-m", "babel.messages.frontend"]
    if exe := shutil.which("pybabel"):
        return [exe]
    if uvx := shutil.which("uvx"):
        return [uvx, "--from", "babel", "pybabel"]
    sys.exit("Babel not found: install it, put pybabel on PATH, or install uv.")


def to_args(options: dict) -> list[str]:
    args = []
    for key, value in options.items():
        flag = "--" + key.replace("_", "-")
        if isinstance(value, bool):
            if value:
                args.append(flag)
        elif isinstance(value, list):
            args += [f"{flag}={v}" for v in value]
        else:
            args.append(f"{flag}={value}")
    return args


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", nargs="?", default="compile", choices=SECTIONS)
    parser.add_argument("--project", type=Path, default=Path.cwd(),
                        help="directory containing pyproject.toml (default: cwd)")
    parser.add_argument("--dry-run", action="store_true", help="print the command only")
    parser.add_argument("extra", nargs="*", help="extra args passed to pybabel (after --)")
    ns = parser.parse_args()

    project = ns.project.resolve()
    pyproject = project / "pyproject.toml"
    if not pyproject.is_file():
        sys.exit(f"{pyproject} not found")

    babel_cfg = tomllib.loads(pyproject.read_text()).get("tool", {}).get("babel", {})
    section = SECTIONS[ns.command]
    options = babel_cfg.get(section)
    if options is None:
        sys.exit(f"[tool.babel.{section}] not found in {pyproject}")

    cmd = [*pybabel_cmd(), ns.command, *to_args(options), *ns.extra]
    if ns.command == "extract" and not ns.extra:
        cmd.append(".")  # extract needs input paths

    print(f"[{project}] {shlex.join(cmd)}", file=sys.stderr)
    if not ns.dry_run:
        sys.exit(subprocess.run(cmd, cwd=project).returncode)


if __name__ == "__main__":
    main()
