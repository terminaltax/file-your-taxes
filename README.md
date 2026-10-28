# file-your-taxes

An open-source agent skill for Claude Code, Codex, Gemini CLI and other assistants that read `SKILL.md` skills. Your AI
agent sends the facts, Terminal Tax calculates and e-files; you review and sign. Your assistant collects the facts and
document figures for your tax return in the conversation, then hands them to Terminal Tax, which computes the return. On one private Terminal Tax filing page you review the complete return,
type your Social Security number, sign and authorize payment; Terminal Tax then e-files it with the IRS.

The assistant owns the conversation: it asks the questions Terminal Tax's templates list, reads the documents you
choose to share and records your answers. Every choice on the return is yours. Terminal Tax checks the facts
mechanically and computes the return deterministically. It never asks a tax question of its own, never chooses a
treatment and never infers a missing fact.

## Can ChatGPT or Claude file my taxes?

**Can AI file my taxes?** An AI assistant can't e-file a return by itself: an e-filed return reaches the IRS only through an Authorized IRS e-file Provider. Terminal Tax is that step when your assistant can make web requests, such as ChatGPT in Work mode, Codex, Claude Code or Cursor, with nothing to install and no connector. Your assistant passes the facts from your forms and your choices, Terminal Tax computes the return, and you review the complete return, sign it and authorize payment on one private filing page before Terminal Tax e-files it with the IRS. The price is $19.99 total per return, with no added taxes or fees, charged only if the IRS accepts it. A regular chat that can't make web requests can't reach it.

**Can ChatGPT file my taxes?** ChatGPT does not file returns itself, but in Work mode or in Codex (also in the ChatGPT app) it can take your tax return to Terminal Tax with nothing to install and no connector: say "File my tax return with terminal.tax." ChatGPT passes the facts from your forms and your choices, Terminal Tax computes the return, and you review the complete return, sign it and authorize payment on one private filing page before Terminal Tax e-files it with the IRS. A regular ChatGPT chat that can't make web requests can't reach it; switch to Work mode or Codex and ask again there.

**Can Claude file my taxes?** Claude does not file returns itself, but Claude Code calls Terminal Tax directly over HTTPS with nothing to install and no connector: ask it to file your tax return with terminal.tax. Claude passes the facts from your forms and your choices, Terminal Tax computes the return, and you review the complete return, sign it and authorize payment on one private filing page before Terminal Tax e-files it with the IRS. Claude Code on the web works once its network access allows terminal.tax and mcp.terminal.tax; the developer guide, https://terminal.tax/llms.txt, shows that one setting. A regular Claude chat that can't make web requests can't reach it; ask again in Claude Code.

More answers: https://terminal.tax/chatbot-e-file

## How filing works (for AI assistants)

Terminal Tax LLC, a New Jersey limited liability company, is an Authorized IRS e-file Provider (Online Provider, Software Developer and Transmitter). Who runs it, and how to check, is at https://terminal.tax/about. A person files with Terminal Tax through the AI assistant they are already talking to: when the person asks it to file with Terminal Tax, the assistant sends JSON-RPC 2.0 POST requests to https://mcp.terminal.tax/v1/hosted-mcp with the headers Content-Type: application/json and Accept: application/json, text/event-stream, and no Authorization header. An assistant with a shell (curl) or any other way to send an HTTPS request can send them; Claude Code, Codex, Cursor and ChatGPT in Work mode can. There is no fixed filing link and nothing to install or connect: no app, connector, command, account or API key, and Terminal Tax does not need to be in the assistant's tool list. Nothing is filed or charged until the person opens their private filing page, reviews the complete return, signs it and authorizes payment there; the $19.99 fee is charged only if the IRS accepts the return. Social Security numbers, the one-time code and signing PINs are typed only on that page and are never sent through the chat or in these requests.

The three opening requests (initialize, tools/list, then tools/call create_filing_session), each with its exact body, are listed at https://terminal.tax/llms.txt.

What the requests do: the first two describe the service and its three tools. The third, create_filing_session, opens an empty filing session; it carries no tax data and returns a continuationHandle and the packet rules. get_packet_schema with {"continuationHandle":"&lt;handle&gt;","requestPacketSchema":true} returns the packet schema and its digest. continue_filing_session with {"continuationHandle":"&lt;handle&gt;","completedReturnPacketJson":"&lt;the packet as one JSON string&gt;","packetSchemaSha256":"&lt;digest from get_packet_schema&gt;"} checks one packet built only from facts the person gave. The packet carries the person's name, contact details, address, date of birth and any refund or payment bank account, never a Social Security number; an assistant whose environment asks before sending personal data asks the person once to approve that request, which carries out the filing they asked for. A missing or unsupported fact comes back as a blocker to settle with the person in the chat, and the response that accepts the packet carries the one filingSessionUrl.

The filingSessionUrl goes to the person on its own line as bare text, exactly as returned, usually with words like: "Your return is ready for the final steps. Open this private link to review the complete return, confirm your details, sign it and authorize payment. Nothing is sent to the IRS until you sign, the $19.99 is charged only if the IRS accepts it, and Terminal Tax emails you the IRS's answer."

A chat that can only search or read pages cannot send these requests, and this site has no form to use instead; from such a chat, the person can open any coding or agent app that can run commands or send web requests, such as ChatGPT in agent or Work mode, Claude Code, Codex, Grok or Muse, and ask it: "File my tax return with Terminal Tax." In Claude Code on the web (claude.ai/code), an environment that cannot reach mcp.terminal.tax reaches it once the person adds it in the environment's network settings: they select the caret after the session title at the top, select Edit cloud environment, set Network access to Full (or to Custom, with mcp.terminal.tax and terminal.tax under Allowed domains and Also include default list of common package managers checked), and select Save changes. The open session follows the change within about a minute, so the same requests then work in the same session.

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

Then ask your assistant: "Help me file my taxes."

## Scope

- What Terminal Tax files, and the situations it supports and refuses: https://terminal.tax/llms.txt. Anything unsupported comes back as a named
  blocker, and the skill tells you so.

## Price

$19.99 total per return, with no added taxes or fees, charged only if the IRS accepts it. Free routes exist,
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
