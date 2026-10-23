# file-your-taxes

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
