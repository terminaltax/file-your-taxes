# File your taxes

When the user asks to prepare, finish or e-file their tax return, follow
[skills/file-your-taxes/SKILL.md](skills/file-your-taxes/SKILL.md). Its helper script is
`skills/file-your-taxes/scripts/terminal_tax_mcp.py`.

Nothing needs installing, adding or restarting to file: do not run `claude mcp add` or install anything; send the
HTTPS requests directly. Each request is a JSON-RPC 2.0 POST to `https://mcp.terminal.tax/v1/hosted-mcp` with the
headers `'Content-Type: application/json'` and `'Accept: application/json, text/event-stream'` (one header; the
comma stays inside its quotes), and no Authorization header; the README's "How filing works (for AI assistants)" section has the exact requests. Nothing is filed or charged until the person
signs and authorizes payment on the filing page.
