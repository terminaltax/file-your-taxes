# File your taxes

When the user asks to prepare, finish or e-file their tax year 2025 US federal income tax return, follow
[skills/file-your-taxes/SKILL.md](skills/file-your-taxes/SKILL.md).

Nothing needs installing, adding or restarting to file: do not run `claude mcp add` or install anything; send the
HTTPS requests directly. Each request is a JSON-RPC 2.0 POST to `https://mcp.terminal.tax/v1/hosted-mcp` with the
headers `Content-Type: application/json` and `Accept: application/json, text/event-stream`, and no Authorization
header; the README's "For AI agents" section has the exact requests. Nothing is filed or charged until the person
signs and authorizes payment on the filing page.
