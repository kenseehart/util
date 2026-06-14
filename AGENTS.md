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
| `gmon` | Reactive directory monitor |
| `stringbreak` | Break debugger on matching output string |
| `yamster` | Reactive YAML store |

## Repo

- Path: **`/home/ken/util`**
- GitHub: [kenseehart/util](https://github.com/kenseehart/util)

## Installation (global editable)

Installed in `~/.local/share/uv/global` with editable package + mkdo wrappers:

```bash
whip util.whip    # should print path to whip.py
mkpy mytool       # create new command module
mkdo mytool       # deploy to global bin
```

Reinstall after clone:

```bash
uv pip install -e /home/ken/util --python ~/.local/share/uv/global/bin/python
~/.local/share/uv/global/bin/python -m util.mkdo_setup
```

## Conventions

- setuptools (`setup.py`) — no pyproject yet
- Commands are `python -m module.name` wrappers, not hashbang scripts
- Edit modules in place; changes reflect immediately (editable install)
