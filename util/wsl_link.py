"""Cross-WSL peer home mounts at /mnt/evolver and /mnt/personal (drvfs)."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

PERSONAL_DISTRO = "Ubuntu-22.04"
EVOLVER_DISTRO = "Ubuntu"

# this distro -> (mount path, peer distro)
PEERS: dict[str, tuple[str, str]] = {
    PERSONAL_DISTRO: ("evolver", EVOLVER_DISTRO),
    EVOLVER_DISTRO: ("personal", PERSONAL_DISTRO),
}


def _in_wsl() -> bool:
    return platform.system() == "Linux" and "microsoft" in platform.release().lower()


def current_distro() -> str | None:
    name = os.environ.get("WSL_DISTRO_NAME", "").strip()
    return name if name in PEERS else None


def unc_home(distro: str) -> str:
    return f"\\\\wsl.localhost\\{distro}\\home\\ken"


def mount_path(distro: str) -> Path:
    name, _ = PEERS[distro]
    return Path("/mnt") / name


def is_mounted(path: Path) -> bool:
    try:
        out = subprocess.check_output(
            ["findmnt", "-n", "-o", "TARGET", str(path)],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip() == str(path)
    except (OSError, subprocess.CalledProcessError):
        return False


def _run(cmd: list[str], *, dry_run: bool) -> bool:
    print("  " + " ".join(cmd))
    if dry_run:
        return True
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def _stale_home_mounts(link_name: str, *, dry_run: bool) -> None:
    home = Path.home() / link_name
    if is_mounted(home):
        print(f"Removing stale mount at {home}")
        _run(["sudo", "umount", str(home)], dry_run=dry_run)


def setup_local(*, dry_run: bool = False) -> int:
    if not _in_wsl():
        print("Not running inside WSL.", file=sys.stderr)
        return 1

    distro = current_distro()
    if not distro:
        print(
            f"Unknown distro (WSL_DISTRO_NAME={os.environ.get('WSL_DISTRO_NAME')!r}). "
            f"Expected {PERSONAL_DISTRO} or {EVOLVER_DISTRO}.",
            file=sys.stderr,
        )
        return 1

    link_name, peer_distro = PEERS[distro]
    mnt = mount_path(distro)
    role = "personal" if distro == PERSONAL_DISTRO else "evolver"

    print(f"Distro: {distro} ({role})")
    print(f"Mount:  {mnt} -> {peer_distro}:/home/ken")

    if is_mounted(mnt):
        print(f"Already mounted at {mnt}")
        return 0

    _stale_home_mounts(link_name, dry_run=dry_run)

    if mnt.exists() and not is_mounted(mnt) and any(mnt.iterdir()):
        print(f"ERROR: {mnt} exists and is not empty.", file=sys.stderr)
        return 1

    if not dry_run:
        mnt.mkdir(parents=True, exist_ok=True)

    print("\nMount:")
    if not _run(
        ["sudo", "mount", "-t", "drvfs", unc_home(peer_distro), str(mnt)],
        dry_run=dry_run,
    ):
        print("Mount failed — run the command above manually.", file=sys.stderr)
        return 1

    if dry_run:
        return 0

    print(f"\nOK: {mnt}")
    print("\nPersist — add to /etc/fstab:")
    print(f"  {unc_home(peer_distro)} {mnt} drvfs defaults 0 0")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Mount peer WSL home at /mnt/evolver or /mnt/personal",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands only")
    parser.add_argument(
        "--both",
        action="store_true",
        help="Also print command for peer distro",
    )
    args = parser.parse_args()
    code = setup_local(dry_run=args.dry_run)
    if code == 0 and args.both:
        distro = current_distro()
        if distro:
            peer = EVOLVER_DISTRO if distro == PERSONAL_DISTRO else PERSONAL_DISTRO
            print(f"\n--- On {peer}, run: ---")
            print("  wsl_link")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
