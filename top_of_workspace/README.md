# Workspace-level config (versioned)

Canonical copies of files that live at `/home/ken/ws` via symlinks.

```bash
init_workspace --force   # after clone or when adding entries to top_of_workspace.json
init_workspace --check   # verify symlinks
```

**Not symlinked** (local secrets / ephemeral): `.cursor/mcp.json`, `.cursor/plans/`

Edit files here; changes apply at the workspace root through symlinks.
