"""Serve workspace SQLite databases in a local Datasette browser UI."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbTarget:
    path: Path


@dataclass(frozen=True)
class DbEntry:
    loader: Callable[[], DbTarget]
    sqlite_vec: bool = False


def _fish_target() -> DbTarget:
    from fish.config import DB_PATH

    return DbTarget(path=DB_PATH)


def _bridge_target() -> DbTarget:
    from bridge.store import DB_PATH

    return DbTarget(path=DB_PATH)


REGISTRY: dict[str, DbEntry] = {
    "fish": DbEntry(_fish_target, sqlite_vec=True),
    "bridge": DbEntry(_bridge_target),
}


def _datasette_bin() -> str:
    path = shutil.which("datasette")
    if not path:
        raise RuntimeError(
            "datasette not found — install with: uv tool install datasette"
        )
    return path


def _vec_extension_path() -> str:
    import sqlite_vec

    return sqlite_vec.loadable_path()


def build_serve_cmd(
    target: DbTarget,
    *,
    sqlite_vec: bool = False,
    host: str = "127.0.0.1",
    port: int = 8001,
) -> list[str]:
    cmd = [
        _datasette_bin(),
        "serve",
        f"--host={host}",
        f"--port={port}",
    ]
    if sqlite_vec:
        cmd.append(f"--load-extension={_vec_extension_path()}")
    cmd.append(str(target.path))
    return cmd


def serve(
    name: str,
    *,
    host: str = "127.0.0.1",
    port: int = 8001,
) -> int:
    key = name.strip().lower()
    entry = REGISTRY.get(key)
    if entry is None:
        known = ", ".join(sorted(REGISTRY))
        raise RuntimeError(f"Unknown database {name!r} — known: {known}")
    target = entry.loader()
    if not target.path.is_file():
        raise RuntimeError(f"Database file not found: {target.path}")
    cmd = build_serve_cmd(
        target, sqlite_vec=entry.sqlite_vec, host=host, port=port
    )
    print(f"Opening {target.path} at http://{host}:{port}/")
    return subprocess.call(cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dbserv",
        description="Browse workspace SQLite databases with Datasette",
    )
    parser.add_argument(
        "database",
        nargs="?",
        help=f"Database name ({', '.join(sorted(REGISTRY))})",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List known databases and paths",
    )
    parser.add_argument("--port", type=int, default=8001, help="HTTP port (default 8001)")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Bind address (default 127.0.0.1 = local only)",
    )
    args = parser.parse_args(argv)

    if args.list:
        for key in sorted(REGISTRY):
            entry = REGISTRY[key]
            try:
                path = entry.loader().path
                status = str(path)
                if not path.is_file():
                    status += " (missing)"
            except Exception as exc:
                status = str(exc)
            vec = " +vec" if entry.sqlite_vec else ""
            print(f"{key}{vec}\t{status}")
        return 0

    if not args.database:
        parser.error("database name required (or use --list)")

    try:
        return serve(args.database, host=args.host, port=args.port)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
