"""Install workspace projects into ~/.local/share/uv/global and mkdo CLIs to ~/.local/bin."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from util.mkdo import mkdo

WORKSPACE = Path.home() / "ws"
GLOBAL_PYTHON = Path.home() / ".local/share/uv/global/bin/python"
LOCAL_BIN = Path.home() / ".local/bin"
GLOBAL_BIN = GLOBAL_PYTHON.parent
GLOBAL_TEMPLATE = "global"

# Editable installs (dependency order). Excludes daime (GPU) and legacy agi.green.
EDITABLE_PACKAGES = [
    WORKSPACE / "util",
    WORKSPACE / "shared/cmdline",
    WORKSPACE / "shared/mcp",
    WORKSPACE / "compute",
    WORKSPACE / "fish",
    WORKSPACE / "host",
    WORKSPACE / "nfnc",
    WORKSPACE / "tesla",
    WORKSPACE / "cristopoly",
    WORKSPACE / "bridge",
]

# mkdo module → command name (default: leaf module name)
COMMANDS: list[str | tuple[str, str]] = [
    "fish",
    "compute",
    "util.wsl_link",
    "util.init_workspace",
    "host.sitehost",
    "nfnc",
    "cristopoly.fetch_streetview",
    "cristopoly.property_map",
    "cristopoly.sync_board_photos",
    "cristopoly.sync_property_names",
    "cristopoly.apply_streetview",
    "cristopoly.hollow_pieces",
]


def _run(cmd: list[str]) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def _is_python_project(path: Path) -> bool:
    return (path / "pyproject.toml").is_file() or (path / "setup.py").is_file()


def install_packages() -> None:
    if not GLOBAL_PYTHON.is_file():
        raise SystemExit(f"global uv python not found: {GLOBAL_PYTHON}")
    for pkg in EDITABLE_PACKAGES:
        if not _is_python_project(pkg):
            raise SystemExit(f"not a Python project: {pkg}")
        _run(["uv", "pip", "install", "-e", str(pkg), "--python", str(GLOBAL_PYTHON)])


def install_commands() -> None:
    LOCAL_BIN.mkdir(parents=True, exist_ok=True)
    _run([str(GLOBAL_PYTHON), "-m", "util.mkdo_setup"])
    for spec in COMMANDS:
        module = spec[0] if isinstance(spec, tuple) else spec
        mkdo(module, str(LOCAL_BIN), template=GLOBAL_TEMPLATE)
    # tesla uses [project.scripts]; pip install -e places tesla-fleet-mcp in global/bin.
    tesla_cmd = GLOBAL_BIN / "tesla-fleet-mcp"
    if not tesla_cmd.is_file():
        mkdo("tesla_mcp", str(LOCAL_BIN), template=GLOBAL_TEMPLATE)


def main() -> int:
    install_packages()
    install_commands()
    print(f"\nGlobal env: {GLOBAL_PYTHON}")
    print(f"Commands:   {LOCAL_BIN} (+ {GLOBAL_BIN} for whip/mkdo/tesla-fleet-mcp)")
    print("Re-run after adding a project: python -m util.global_setup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
