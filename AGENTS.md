# Agent onboarding — util

## Shared resources

Workspace index: **`/home/ken/AGENTS.md`**.

## What this project is

Old-school Python CLI utilities deployed via wrapper scripts:

| Command | Purpose |
|---------|---------|
| `whip` | Locate a Python module (like `which` for imports) |
| `mkdo` | Install a module as an executable in `bin/` |
| `mkpy` | Scaffold a new command module |
| `mkdo_setup` | Bootstrap whip/mkdo/mkpy into a venv (`python -m util.mkdo_setup`) |
| `gmon` | Reactive directory monitor |
| `stringbreak` | Break debugger on matching output string |
| `yamster` | Reactive YAML store |

## Repo

- Path: **`/home/ken/util`**
- GitHub: [kenseehart/util](https://github.com/kenseehart/util)

## Installation (global editable)

All lightweight workspace projects install into **`~/.local/share/uv/global`**. Refresh everything:

```bash
global_setup    # python -m util.global_setup
```

Or manually:

```bash
uv pip install -e /home/ken/util --python ~/.local/share/uv/global/bin/python
mkdo_setup
mkdo mytool -d ~/.local/bin -t global
```

| Command | Purpose |
|---------|---------|
| `whip` | Locate a Python module (like `which` for imports) |
| `mkdo` | Install a module as an executable in `bin/` |
| `mkpy` | Scaffold a new command module |
| `mkdo_setup` | Bootstrap whip/mkdo/mkpy/global_setup into global bin |
| `global_setup` | Install all workspace packages + CLIs (see `global_setup.py`) |

After `uv sync` in a **project venv** (optional isolated dev): `uv run python -m util.mkdo_setup` then `mkdo <package> -d .venv/bin`. Prefer global env for daily use.

Reinstall after clone:

```bash
global_setup
```

## Conventions

- setuptools (`setup.py`) — no pyproject yet
- Commands are `python -m module.name` wrappers, not hashbang scripts
- Edit modules in place; changes reflect immediately (editable install)
