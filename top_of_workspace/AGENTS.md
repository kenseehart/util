# Agent onboarding — Ken workspace (`/home/ken/ws`)

Multi-project AI development workspace. **Open `/home/ken/ws` in Cursor** (or `ken.code-workspace`) — not `~`, which duplicates MCP config.

Open this file at the start of any cross-project session.

## Project map

| Dir | GitHub | Purpose | AGENTS.md |
|-----|--------|---------|-----------|
| `shared/` | kenseehart/shared | Cross-project UI, MCP templates, scaffolding | ✓ |
| `daime/` | kenseehart/daime | Hinario — hymn analysis, GPU ASR, player | ✓ (detailed) |
| `tesla/` | kenseehart/tesla-mcp (fork of ysrdevs/tesla-mcp) | Tesla Fleet MCP (96 tools) | ✓ |
| `nfnc/` | kenseehart/nfnc | Google Sheets MCP + CLI | ✓ |
| `util/` | kenseehart/util | Shell-adjacent Python CLI tools (whip, mkdo, mkpy) | ✓ |
| `agi.green/` | kenseehart/agi.green | **Legacy** chat framework — reference only | ✓ |
| `fish/` | kenseehart/imap_sorting_hat | IMAP email AI | ✓ |
| `y/` | kenseehart/y | Game of Y | ✓ |
| `host/` | kenseehart/host | Static site scaffold, rsync deploy, Host MCP | ✓ |
| `compute/` | kenseehart/compute | On-demand VM/container management (`compute` CLI) | ✓ |
| `upscale/` | kenseehart/upscale | GPU batch consumer (uses compute) | ✓ |
| `seehart/` | kenseehart/seehart | seehart.com site (scaffold) | ✓ |
| `cristopoly/` | kenseehart/cristopoly | Custom Monopoly board | ✓ |

## Shared resources

**`/home/ken/ws/shared`** — one repo for cross-project assets. Do not duplicate chat CSS/JS into each site; link or copy from here.

| Resource | Path |
|----------|------|
| Claude-style chat widget | `shared/web/chat/agi-chat.{js,css}` |
| New project AGENTS template | `shared/templates/AGENTS.project.md` |
| Cursor rule template | `shared/templates/project.mdc` |
| FastMCP starter | `shared/mcp/starter_server.py` |
| OAuth personal auth | `shared/mcp` (`ken-mcp` package) — `PersonalAuthProvider` |
| GitHub MCP (shared) | `shared/mcp/github/` — install via `install.sh` |

## MCP servers (Cursor)

Configured in **`/home/ken/ws/.cursor/mcp.json`** (project scope). Global `~/.cursor/mcp.json` is intentionally empty so Cursor does not duplicate servers when workspace root is not `~`. All local MCP servers use **`~/.local/share/uv/global/bin/python`** (shared workspace env):

| Server | Command | Phone-ready |
|--------|---------|-------------|
| github | Remote `api.githubcopilot.com/mcp/` | PAT only (see `shared/mcp/github/`) |
| tesla | `~/.local/share/uv/global/bin/tesla-fleet-mcp` | Yes (OAuth on hosting) |
| nfnc | `global/bin/python -m nfnc.mcp_server` | Needs OAuth deploy |
| fish | `global/bin/python -m fish.mcp_server` | Needs OAuth deploy |

## Global Python environment

One shared uv env at **`~/.local/share/uv/global`** holds all lightweight workspace packages (editable). Commands are on PATH via **`~/.local/bin/env`** (sourced from `~/.bashrc` / `~/.profile`).

| Path | Contents |
|------|----------|
| `~/.local/share/uv/global/bin/` | `whip`, `mkdo`, `mkpy`, `tesla-fleet-mcp`, … |
| `~/.local/bin/` | Project CLIs (`fish`, `sitehost`, `compute`, `nfnc`, `fetch_streetview`, …) |

**Exception:** **`daime`** keeps its own `.venv` (GPU/torch). Do not install daime into global.

### Bootstrap / refresh

After cloning or adding a project:

```bash
global_setup    # or: python -m util.global_setup
init_workspace --force
```

This runs `uv pip install -e` for util, shared/cmdline, shared/mcp, compute, fish, host, nfnc, tesla, cristopoly, then `mkdo -t global -d ~/.local/bin` for each CLI.

Add a new project: edit `util/global_setup.py` (`EDITABLE_PACKAGES` + `COMMANDS`), then re-run `global_setup`.

Per-project `.venv` dirs are optional (isolated dev); daily use needs no activation.

## Global CLI tools

| Command | Purpose |
|---------|---------|
| `compute` | On-demand VM/container management (GCP, RunPod, local) |
| `whip <module>` | Locate a Python module (like `which` for imports) |
| `mkdo <package>` | Install `python -m` wrapper as a command in `bin/` |
| `mkpy <name>` | Scaffold a new command module |
| `mkdo_setup` | Bootstrap whip/mkdo/mkpy into the active venv |
| `global_setup` | Install all workspace packages + CLIs into shared global env |
| `init_workspace` | Symlink workspace Cursor rules and AGENTS.md from `util/top_of_workspace` |

```bash
fish sync
sitehost deploy --dry-run
whip host.sitehost
```

Prefer **`sitehost`**, **`fish`**, etc. over bare `host` or `uv run python -m …` — bare `host` is the system DNS tool (`/usr/bin/host`).

Reinstall util only: `uv pip install -e /home/ken/ws/util --python ~/.local/share/uv/global/bin/python && mkdo_setup`

## Hosting

Everything deploys to **[my.hosting.com](https://my.hosting.com/)** (unlimited domains).

- **Static sites**: `host` CLI — rsync per `host.yaml` manifest ([`/home/ken/ws/host`](/home/ken/ws/host))
- **Thin Python MCP**: hosting.com Python app — [`host/docs/hosting-python.md`](/home/ken/ws/host/docs/hosting-python.md)
- **Heavy compute**: `compute` CLI — GCP / RunPod ([`/home/ken/ws/compute`](/home/ken/ws/compute))
- **Host MCP**: Claude.ai site management at `seehart.com/host/mcp` (connectors deferred until MCP experiment passes)

## Subscriptions & billing

Cross-project audit of cloud/AI subscriptions (fish mail search, cancel list, annual totals): **`docs/billing-subscriptions.md`**.

## Conventions

1. **Python**: `uv` + `pyproject.toml` per project
2. **Agent docs**: `AGENTS.md` per repo; ops detail in `.cursor/rules/*.mdc`
3. **Web**: static HTML + `shared/web/chat/` — no WIX, no mandatory npm
4. **MCP**: FastMCP pattern (`nfnc`, `tesla`, `shared/mcp/starter_server.py`)
5. **Legacy**: agi.green full stack is deprecated for new work — see `agi.green/AGENTS.md`

## Starting a project-specific session

Open the project's `AGENTS.md` and mention the project name in your first message. Example: *"Working on fish — scaffold IMAP MCP tools."*
