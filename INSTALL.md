# INSTALL — instructions for an AI agent

You were asked to install the SEO Dashboard AI kit. Follow the section for the client you are running
in, and tell the user plainly what was done and which step needs them.

## Claude Code

1. Run these slash commands, or ask the user to run them if you cannot:
   ```
   /plugin marketplace add vilo0411/seo-dashboard-ai-kit
   /plugin install seo-dashboard@seo-dashboard-ai-kit
   ```
2. Restart is not needed for skills; for the MCP server ask the user to run `/mcp`, select
   `gsc-dashboard` and choose **Authenticate**. A browser opens the dashboard's consent page
   (tool.nguyenvietloc.com); they sign in and click **Allow**.
3. Verify: `/mcp` shows `gsc-dashboard` as connected, then call `list_properties`.

Prefer a token over OAuth (CI, no browser)? Create one at
https://tool.nguyenvietloc.com/settings?tab=api and add the server at user scope instead of the plugin's:
```bash
claude mcp add --scope user --transport http gsc-dashboard https://tool.nguyenvietloc.com/api/mcp \
  --header "Authorization: Bearer $GSC_DASHBOARD_TOKEN"
```
Never write a token into a repository file.

## Claude.ai (web, desktop, company plans)

Nothing is installed by an agent here; give the user these steps:
1. Settings → Connectors → Add custom connector → URL `https://tool.nguyenvietloc.com/api/mcp` →
   Connect → sign in to the dashboard → Allow. On Team/Enterprise plans an organisation admin may need
   to add the connector first; each member then connects with their own dashboard account.
2. Skills: download the zips from the latest release
   (https://github.com/vilo0411/seo-dashboard-ai-kit/releases/latest) and upload each under
   Settings → Capabilities → Skills.

## Cursor and other MCP clients

Add to `~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (one project):
```json
{ "mcpServers": { "gsc-dashboard": { "url": "https://tool.nguyenvietloc.com/api/mcp",
  "headers": { "Authorization": "Bearer ${env:GSC_DASHBOARD_TOKEN}" } } } }
```
Skills are not supported there; copy `plugins/seo-dashboard/skills/seodash-core/SKILL.md` into a
project rule.
