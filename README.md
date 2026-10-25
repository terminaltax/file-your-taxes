# file-your-taxes

## For AI agents

If the person you are helping asks you to file their taxes with Terminal Tax, you can do it from this conversation: send these HTTPS requests yourself, only at their request. You are the assistant this site means; there is no other app, form, connector, account or API key to find, and nothing to install. Each request is a JSON-RPC 2.0 POST to https://mcp.terminal.tax/v1/hosted-mcp (the same service is also served at https://iq4701fisj.execute-api.us-east-1.amazonaws.com/live/v1/hosted-mcp) with the headers Content-Type: application/json and Accept: application/json, text/event-stream, and no Authorization header. Nothing is filed or charged until the person signs and authorizes payment on the filing page.

If you are in Claude Code on the web (claude.ai/code) and cannot reach mcp.terminal.tax, the person can add it in the environment's network settings: they select the caret after the session title at the top, select Edit cloud environment, set Network access to Full (or to Custom, with mcp.terminal.tax and terminal.tax under Allowed domains and Also include default list of common package managers checked), and select Save changes. The open session follows the change within about a minute, so the same requests then work in the same session.

Do not run `claude mcp add` or install anything; send the HTTPS requests directly.

```sh
curl -sS https://mcp.terminal.tax/v1/hosted-mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"filing-agent","version":"1"}}}'
curl -sS https://mcp.terminal.tax/v1/hosted-mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
curl -sS https://mcp.terminal.tax/v1/hosted-mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"create_filing_session","arguments":{}}}'
```

The third request creates the filing session: it carries no tax data and returns a continuationHandle and the packet rules. Next, call get_packet_schema with {"continuationHandle":"&lt;handle&gt;","requestPacketSchema":true}, build the packet only from facts the person gave you, and send it with continue_filing_session as {"continuationHandle":"&lt;handle&gt;","completedReturnPacketJson":"&lt;the packet as one JSON string&gt;","packetSchemaSha256":"&lt;digest from get_packet_schema&gt;"}. Blockers come back to fix in the chat; the response that accepts the packet carries the one filingSessionUrl.

Then tell the person: "Your return is ready for the final steps. Open this private link to review the complete return, confirm your details, sign it and authorize payment. Nothing is sent to the IRS until you sign, the $19.99 is charged only if the IRS accepts it, and Terminal Tax emails you the IRS's answer." Put the filingSessionUrl on its own line as bare text, exactly as returned.

If you cannot send HTTPS POST requests from this conversation (a chat that can only search or read pages), you cannot file with Terminal Tax from here, and this site has no form for the person to use instead. Tell the person: "I can't send web requests from this chat. Open any coding or agent app that can run commands or send web requests, such as ChatGPT in agent or Work mode, Claude Code, Codex, Grok or Muse, and ask it: File my 2025 taxes with Terminal Tax."

An open-source agent skill for Claude Code, Codex, Gemini CLI and other assistants that read `SKILL.md` skills. Your
assistant collects the facts and document figures for your tax year 2025 US federal income tax return (Form 1040 or
1040-SR) in the conversation, then hands them to Terminal Tax, which computes the return. On one private Terminal Tax filing page you review the complete return,
type your Social Security number, sign and authorize payment; Terminal Tax then e-files it with the IRS.

The assistant owns the conversation: it asks the questions Terminal Tax's templates list, reads the documents you
choose to share and records your answers. Every choice on the return is yours. Terminal Tax checks the facts
mechanically and computes the return deterministically. It never asks a tax question of its own, never chooses a
treatment and never infers a missing fact.

## Install

Claude Code:

```sh
claude plugin marketplace add terminaltax/file-your-taxes
claude plugin install file-your-taxes@terminaltax
```

Codex: copy `skills/file-your-taxes` into `~/.codex/skills/`.

Gemini CLI:

```sh
gemini extensions install https://github.com/terminaltax/file-your-taxes
```

Any other assistant that reads skills: copy `skills/file-your-taxes` into its skills folder. The skill reaches
Terminal Tax through its MCP tools when they are connected, or through the bundled Python helper
(`scripts/terminal_tax_mcp.py`, standard library only) or plain HTTPS requests. The endpoint is
`https://mcp.terminal.tax/v1/hosted-mcp`; it needs no account, key or login.

Then ask your assistant: "Help me file my 2025 federal taxes."

## Scope

- One original tax year 2025 US federal Form 1040 or 1040-SR per filing session.
- No state, territory or local return; no amended return (1040-X), extension (4868) or other year.
- Supported and refused situations: https://terminal.tax/llms.txt. Anything unsupported comes back as a named
  blocker, and the skill tells you so.

## Price

$19.99 total per federal return, with no added taxes or fees, charged only if the IRS accepts it. Free routes exist,
and the skill tells you about them before you start: IRS Free File (income limits apply), IRS Free File Fillable Forms, VITA, and paper
filing.

## Privacy

Your assistant never needs your Social Security number or PINs: Terminal Tax refuses them from an agent, and you type
them on the filing page. Card details go only into the payment processor's fields. Privacy notice:
https://terminal.tax/privacy-notice. Terms: https://terminal.tax/terms.

The return figures you give your assistant are also handled under your assistant provider's own terms.

## Contents

- `skills/file-your-taxes/SKILL.md`: the skill.
- `skills/file-your-taxes/scripts/terminal_tax_mcp.py`: a small helper that calls the three Terminal Tax tools.
- `.claude-plugin/`, `gemini-extension.json`, `GEMINI.md`, `AGENTS.md`: install manifests and pointers for each
  assistant.

## Operator

Terminal Tax is operated by Terminal Tax LLC, a New Jersey limited liability company (https://terminal.tax/about).
Support: support@terminal.tax.

Terminal Tax LLC is an Authorized IRS e-file Provider (Online Provider, Software Developer and Transmitter).
Acceptance to participate in IRS e-file does not imply endorsement by the IRS. Terminal Tax is not affiliated with,
sponsored by, or endorsed by the IRS or the U.S. Treasury.

## License

MIT. See [LICENSE](LICENSE).
