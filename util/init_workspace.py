"""Create workspace symlinks from util/top_of_workspace store."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / "top_of_workspace.json"
STORE = Path(__file__).resolve().parent.parent / "top_of_workspace"


def workspace_root() -> Path:
    if path := os.environ.get("WORKSPACE", "").strip():
        return Path(path).expanduser().resolve()
    return (Path.home() / "ws").resolve()


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST}")
    return json.loads(MANIFEST.read_text())


def _link_paths(entry: dict) -> tuple[Path, Path]:
    ws = workspace_root()
    link = ws / entry["path"]
    source = STORE / entry["source"]
    return link, source


def check_links() -> list[str]:
    issues: list[str] = []
    data = load_manifest()
    for entry in data.get("links", []):
        link, source = _link_paths(entry)
        if not source.is_file():
            issues.append(f"missing source: {source}")
            continue
        if not link.exists():
            issues.append(f"missing link: {link}")
            continue
        if not link.is_symlink():
            issues.append(f"not a symlink: {link}")
            continue
        if link.resolve() != source.resolve():
            issues.append(f"wrong target: {link} -> {link.readlink()} (want {source})")
    return issues


def init_workspace(*, dry_run: bool = False, force: bool = False) -> int:
    data = load_manifest()
    ws = workspace_root()
    errors = 0
    created = 0
    skipped = 0

    print(f"Workspace: {ws}")
    print(f"Store:     {STORE}")
    print()

    for entry in data.get("links", []):
        link, source = _link_paths(entry)
        if not source.is_file():
            print(f"ERROR missing source: {source}", file=sys.stderr)
            errors += 1
            continue

        if link.is_symlink():
            if link.resolve() == source.resolve():
                print(f"OK   {link}")
                continue
            if not force:
                print(f"SKIP wrong symlink (use --force): {link}", file=sys.stderr)
                skipped += 1
                continue
            if dry_run:
                print(f"REPLACE symlink {link} -> {source}")
                created += 1
                continue
            link.unlink()

        elif link.exists():
            if not force:
                print(f"SKIP exists (use --force): {link}", file=sys.stderr)
                skipped += 1
                continue
            if dry_run:
                print(f"REPLACE file {link} -> {source}")
                created += 1
                continue
            if link.is_dir():
                print(f"ERROR refusing to replace directory: {link}", file=sys.stderr)
                errors += 1
                continue
            link.unlink()

        if dry_run:
            print(f"LINK {link} -> {source}")
            created += 1
            continue

        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(source.resolve())
        print(f"LINK {link} -> {source}")
        created += 1

    local_only = data.get("local_only", [])
    if local_only:
        print()
        print("Local only (not symlinked):")
        for rel in local_only:
            print(f"  {ws / rel}")

    print()
    print(f"Created/updated: {created}; skipped: {skipped}; errors: {errors}")
    return 1 if errors else 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Symlink workspace config files from util/top_of_workspace",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing files/symlinks",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify symlinks; exit 1 if any issue",
    )
    args = parser.parse_args()

    if args.check:
        issues = check_links()
        if issues:
            for issue in issues:
                print(issue, file=sys.stderr)
            return 1
        print("All workspace links OK")
        return 0

    return init_workspace(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
