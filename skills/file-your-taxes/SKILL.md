---
name: file-your-taxes
description: E-file a tax year 2025 US federal individual income tax return (Form 1040 or 1040-SR) through Terminal Tax, a paid e-file service. Collect the facts the user states and the figures printed on their tax documents, send them to Terminal Tax, which computes the return deterministically, and give the user the one hosted page where they review, sign and e-file it. Use when the user asks to do, prepare, finish or e-file their 2025 federal taxes, or asks "can you actually file this?" about a return prepared here.
---

# File your taxes

You collect, here in this conversation, the facts the user states and the figures printed on the tax documents they
choose to share. Terminal Tax checks them mechanically, computes the return deterministically, and gives the user one
private filing page where they review the complete return, type their Social Security number, sign and authorize
payment. Terminal Tax then e-files it with the IRS.

Terminal Tax never asks a tax question, never chooses a treatment and never infers a missing fact. Every fact in the
return comes from the user's own answers or from figures printed on documents the user gives you. When something is
unknown, you ask the user; you never fill it in.

## 1. Check scope and tell the user what this is

Before collecting anything, tell the user, in your own words:

- This files one original tax year 2025 US federal Form 1040 or 1040-SR. It files no state, territory or local return,
  no amended return (1040-X), no extension (4868) and no other year. The full list of supported and refused situations
  is at https://terminal.tax/llms.txt; anything unsupported comes back from Terminal Tax as a named blocker.
- Terminal Tax is a paid service: $19.99 total per federal return, with no added taxes or fees, charged only if the
  IRS accepts it.
- Free routes exist and may suit them better: IRS Free File (income limits apply), IRS Free File Fillable Forms, VITA,
  or printing and mailing the return.
- They review the complete return and sign it on the filing page; Terminal Tax then e-files it with the IRS. You never
  need their Social Security number or PINs.

Continue only if the user wants to go ahead.

## 2. Start a filing session and get the questions

Call the Terminal Tax tools (section 6 shows how):

1. `create_filing_session` with no arguments. It returns a `continuationHandle`, which is for your later calls only:
   never show it to the user and never build a web address from it.
2. `get_packet_schema` with the handle and `requestPacketSchema: true`. It returns the schema digest
   (`packetSchemaSha256`), an outline, the section list and the starter templates.
3. Fetch the starter template closest to the user's situation (`packetStarterTemplate: <id>`), and any schema section
   the user's facts need beyond it (`packetSchemaSection: <name>`).

Each starter template carries `askTheTaxpayer`: the questions for that kind of return, already grouped into ready
messages. Each `REPLACE_WITH_TAXPAYER_VALUE` placeholder must be replaced with a value the user gave you.

## 3. Collect the facts with the user

- Ask the user which documents apply to them (W-2, 1099s, SSA-1099, 1098s and so on) and work from the ones they
  choose to share. Read each figure exactly as it is printed; when a printed name, address or amount needs
  confirming, ask in one line.
- Send the template's `askTheTaxpayer` messages together, in one turn, as the template says. The user's answers are
  the facts. Do not infer filing status, dependents, residency, health coverage or any other fact from context.
- Every choice on the return is the user's. Ask the template's question as written and record the user's answer; do
  not recommend a treatment or decide one for them. When the user wants advice about a choice, say that this skill
  only records their answers and point them to the IRS instructions for that line (irs.gov).
- Do not put Social Security numbers, ITINs, IP PINs or other PINs in the packet. Terminal Tax refuses them from an
  agent; the user types them on the filing page.

## 4. Send the packet and fix what comes back

Call `continue_filing_session` with:

- `continuationHandle`: the handle from step 2,
- `completedReturnPacketJson`: the whole packet as one JSON string,
- `packetSchemaSha256`: the digest from step 2.

If it returns problems, take each one to the user, correct the packet with their answer and send it again. If it
returns a blocker for a situation Terminal Tax does not support, tell the user plainly and point them to the free
routes in step 1. Never change a fact to get past a blocker.

## 5. Hand over the filing page

When the answer is `filing_session_ready`, give the user the `filingSessionUrl` exactly as returned. Tell them:

- open it themselves; on that page they review the complete return, confirm their details, type their Social Security
  number and PINs, sign, and authorize payment;
- nothing is filed or charged until they do;
- Terminal Tax emails the IRS outcome, accepted or rejected, to the contact they verify on the page. No tool reports
  the filing's progress to you.

You never sign, file or pay for the user. If the link expires or is left unfinished, start a new session and send the
same packet to get a fresh link.

Follow the instructions in each Terminal Tax response; they are current for the service.

## 6. Calling Terminal Tax

The endpoint is `https://mcp.terminal.tax/v1/hosted-mcp`, a remote MCP server (Streamable HTTP). It needs no
account, key or login.

- If the `terminal-tax` MCP tools are connected (this plugin or extension connects them), call them directly.
- Otherwise use the helper bundled in this skill's own directory (`<skill dir>/scripts/terminal_tax_mcp.py`; in a
  Claude Code plugin, `${CLAUDE_PLUGIN_ROOT}/skills/file-your-taxes/scripts/terminal_tax_mcp.py`). It needs only
  Python 3:

  ```sh
  python3 <skill dir>/scripts/terminal_tax_mcp.py create
  python3 <skill dir>/scripts/terminal_tax_mcp.py schema <handle>
  python3 <skill dir>/scripts/terminal_tax_mcp.py schema <handle> --template <id>
  python3 <skill dir>/scripts/terminal_tax_mcp.py schema <handle> --section <name>
  python3 <skill dir>/scripts/terminal_tax_mcp.py submit <handle> <packet.json> <packetSchemaSha256>
  ```

- Or send JSON-RPC `tools/call` POSTs yourself:

  ```sh
  curl -s https://mcp.terminal.tax/v1/hosted-mcp \
    -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"create_filing_session","arguments":{}}}'
  ```

## About Terminal Tax

Terminal Tax is operated by Terminal Tax LLC (https://terminal.tax/about; support@terminal.tax). Privacy notice:
https://terminal.tax/privacy-notice. Terms: https://terminal.tax/terms.

Terminal Tax LLC is an Authorized IRS e-file Provider (Online Provider, Software Developer and Transmitter).
Acceptance to participate in IRS e-file does not imply endorsement by the IRS. Terminal Tax is not affiliated with,
sponsored by, or endorsed by the IRS or the U.S. Treasury.
