#!/usr/bin/env python3
"""Call the Terminal Tax MCP tools with plain JSON-RPC POSTs. Python 3 standard library only.

  terminal_tax_mcp.py create
  terminal_tax_mcp.py schema HANDLE [--template ID | --section NAME]
  terminal_tax_mcp.py submit HANDLE PACKET_JSON_FILE PACKET_SCHEMA_SHA256

Prints the tool result as JSON: the structured result first, then each text message.
TERMINAL_TAX_MCP_URL overrides the endpoint (default https://mcp.terminal.tax/v1/hosted-mcp).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINT = os.environ.get("TERMINAL_TAX_MCP_URL", "https://mcp.terminal.tax/v1/hosted-mcp")


def call(name, arguments):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    ).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
            "user-agent": "file-your-taxes-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as error:
        return {"error": {"message": f"could not reach {ENDPOINT}: {error}"}}
    stripped = raw.lstrip()
    if stripped.startswith("event:") or stripped.startswith("data:"):
        # Server-sent events: each event's data lines form one JSON message; the JSON-RPC reply is the last one.
        events = []
        for block in raw.replace("\r\n", "\n").split("\n\n"):
            data = "\n".join(line[5:].lstrip() for line in block.splitlines() if line.startswith("data:"))
            if data:
                events.append(data)
        raw = events[-1] if events else ""
    try:
        return json.loads(raw)
    except ValueError:
        return {"error": {"message": "the endpoint did not answer with JSON", "body": raw[:2000]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("create", help="create_filing_session")
    schema = sub.add_parser("schema", help="get_packet_schema")
    schema.add_argument("handle")
    which = schema.add_mutually_exclusive_group()
    which.add_argument("--template", help="packetStarterTemplate id")
    which.add_argument("--section", help="packetSchemaSection name")
    submit = sub.add_parser("submit", help="continue_filing_session")
    submit.add_argument("handle")
    submit.add_argument("packet_file", help="file holding the completed return packet JSON")
    submit.add_argument("sha256", help="packetSchemaSha256 from get_packet_schema")
    args = parser.parse_args()

    if args.command == "create":
        reply = call("create_filing_session", {})
    elif args.command == "schema":
        arguments = {"continuationHandle": args.handle}
        if args.template:
            arguments["packetStarterTemplate"] = args.template
        elif args.section:
            arguments["packetSchemaSection"] = args.section
        else:
            arguments["requestPacketSchema"] = True
        reply = call("get_packet_schema", arguments)
    else:
        with open(args.packet_file, encoding="utf-8") as handle:
            packet = json.load(handle)
        reply = call(
            "continue_filing_session",
            {
                "continuationHandle": args.handle,
                "completedReturnPacketJson": json.dumps(packet, separators=(",", ":")),
                "packetSchemaSha256": args.sha256,
            },
        )

    if "result" not in reply:
        json.dump(reply, sys.stdout, indent=2)
        print()
        return 1
    result = reply["result"]
    out = {"structuredContent": result.get("structuredContent"), "messages": []}
    for item in result.get("content", []):
        if item.get("type") == "text":
            out["messages"].append(item["text"])
    if result.get("isError"):
        out["isError"] = True
    json.dump(out, sys.stdout, indent=2)
    print()
    return 1 if result.get("isError") else 0


if __name__ == "__main__":
    sys.exit(main())
