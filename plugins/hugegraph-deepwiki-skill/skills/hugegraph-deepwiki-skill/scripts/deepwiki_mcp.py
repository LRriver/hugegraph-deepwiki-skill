#!/usr/bin/env python3
"""Small DeepWiki MCP client for repository-scoped Q&A."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional


DEFAULT_ENDPOINT = "https://mcp.deepwiki.com/mcp"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPOS_PATH = SKILL_DIR / "references" / "repos.json"


class McpError(RuntimeError):
    pass


def load_repos() -> dict[str, dict[str, Any]]:
    with REPOS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def resolve_repo(alias_or_name: str) -> str:
    repos = load_repos()
    profile = repos.get(alias_or_name)
    if profile is None:
        known = ", ".join(sorted(repos))
        raise McpError(f"Unknown repository alias '{alias_or_name}'. Known aliases: {known}.")
    if not profile.get("enabled", False):
        raise McpError(
            f"Repository alias '{alias_or_name}' is reserved but not enabled yet "
            f"({profile.get('repoName')})."
        )
    return str(profile["repoName"])


def parse_json(data: str) -> dict[str, Any]:
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as exc:
        raise McpError(f"DeepWiki MCP returned non-JSON content: {data[:500]}") from exc
    if not isinstance(parsed, dict):
        raise McpError(f"DeepWiki MCP returned an unexpected JSON payload: {data[:500]}")
    return parsed


def read_sse_response(response: Any, expected_id: Optional[int]) -> dict[str, Any]:
    data_lines: list[str] = []
    seen_payloads: list[str] = []
    max_seconds = float(os.environ.get("DEEPWIKI_MCP_STREAM_TIMEOUT", "60"))
    deadline = time.monotonic() + max_seconds

    while True:
        if time.monotonic() > deadline:
            break
        raw_line = response.readline()
        if not raw_line:
            break

        line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
            continue
        if line:
            continue

        if not data_lines:
            continue

        data = "\n".join(data_lines)
        data_lines = []
        seen_payloads.append(data)
        parsed = parse_json(data)
        if expected_id is None or parsed.get("id") == expected_id:
            return parsed

    if data_lines:
        data = "\n".join(data_lines)
        seen_payloads.append(data)
        parsed = parse_json(data)
        if expected_id is None or parsed.get("id") == expected_id:
            return parsed

    preview = "\n".join(seen_payloads[-3:])
    raise McpError(
        f"DeepWiki MCP stream ended without response id {expected_id} "
        f"within {max_seconds:.0f}s: {preview[:500]}"
    )


class McpClient:
    def __init__(self, endpoint: str, protocol_version: str) -> None:
        self.endpoint = endpoint
        self.protocol_version = protocol_version
        self.session_id: Optional[str] = None
        self.next_id = 1

    def request(self, payload: dict[str, Any], expect_response: bool = True) -> Optional[dict[str, Any]]:
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "Mcp-Protocol-Version": self.protocol_version,
            "User-Agent": "hugegraph-deepwiki-skill/0.1.2",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        req = urllib.request.Request(self.endpoint, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                session_id = response.headers.get("Mcp-Session-Id")
                if session_id:
                    self.session_id = session_id
                if not expect_response:
                    return None
                content_type = response.headers.get("Content-Type", "")
                if "text/event-stream" in content_type:
                    parsed = read_sse_response(response, payload.get("id"))
                else:
                    text = response.read().decode("utf-8")
                    if not text.strip():
                        raise McpError("DeepWiki MCP returned an empty response.")
                    parsed = parse_json(text)
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise McpError(f"DeepWiki MCP HTTP {exc.code}: {details}") from exc
        except urllib.error.URLError as exc:
            raise McpError(f"Could not reach DeepWiki MCP endpoint: {exc.reason}") from exc

        if "error" in parsed:
            raise McpError(f"DeepWiki MCP error: {json.dumps(parsed['error'], ensure_ascii=False)}")
        return parsed

    def rpc(self, method: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": self.next_id, "method": method}
        self.next_id += 1
        if params is not None:
            payload["params"] = params
        result = self.request(payload)
        if result is None:
            raise McpError(f"DeepWiki MCP returned no response for {method}.")
        return result

    def notify(self, method: str, params: Optional[dict[str, Any]] = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self.request(payload, expect_response=False)

    def initialize(self) -> None:
        self.rpc(
            "initialize",
            {
                "protocolVersion": self.protocol_version,
                "capabilities": {},
                "clientInfo": {"name": "hugegraph-deepwiki-skill", "version": "0.1.2"},
            },
        )
        self.notify("notifications/initialized", {})

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        response = self.rpc("tools/call", {"name": name, "arguments": arguments})
        return response.get("result")


def extract_text(result: Any) -> str:
    if isinstance(result, dict):
        content = result.get("content")
        if isinstance(content, list):
            chunks: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        chunks.append(text)
                    elif item.get("type") == "json":
                        chunks.append(json.dumps(item, ensure_ascii=False, indent=2))
            if chunks:
                return "\n\n".join(chunks)
        if "structuredContent" in result:
            return json.dumps(result["structuredContent"], ensure_ascii=False, indent=2)
    return json.dumps(result, ensure_ascii=False, indent=2)


def output_tool_result(client: McpClient, tool: str, arguments: dict[str, Any]) -> None:
    client.initialize()
    result = client.call_tool(tool, arguments)
    print(extract_text(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ask the official DeepWiki MCP server.")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("DEEPWIKI_MCP_ENDPOINT", DEFAULT_ENDPOINT),
        help=f"DeepWiki MCP endpoint. Defaults to {DEFAULT_ENDPOINT}.",
    )
    parser.add_argument(
        "--protocol-version",
        default=os.environ.get("DEEPWIKI_MCP_PROTOCOL_VERSION", "2025-06-18"),
        help="MCP protocol version to send during initialize.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask", help="Ask a repository question.")
    ask.add_argument("--repo", default="hugegraph", help="Repository alias.")
    ask.add_argument("--question", required=True, help="Question to ask DeepWiki.")

    structure = subparsers.add_parser("structure", help="Read wiki structure.")
    structure.add_argument("--repo", default="hugegraph", help="Repository alias.")

    contents = subparsers.add_parser("contents", help="Read wiki contents.")
    contents.add_argument("--repo", default="hugegraph", help="Repository alias.")

    tools = subparsers.add_parser("tools", help="List MCP tools for troubleshooting.")
    tools.set_defaults(command="tools")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    client = McpClient(args.endpoint, args.protocol_version)

    try:
        if args.command == "ask":
            repo_name = resolve_repo(args.repo)
            output_tool_result(
                client,
                "ask_question",
                {"repoName": repo_name, "question": args.question},
            )
        elif args.command == "structure":
            repo_name = resolve_repo(args.repo)
            output_tool_result(client, "read_wiki_structure", {"repoName": repo_name})
        elif args.command == "contents":
            repo_name = resolve_repo(args.repo)
            output_tool_result(client, "read_wiki_contents", {"repoName": repo_name})
        elif args.command == "tools":
            client.initialize()
            print(json.dumps(client.rpc("tools/list", {}).get("result"), ensure_ascii=False, indent=2))
        else:
            parser.error(f"Unhandled command {args.command}")
    except McpError as exc:
        print(f"deepwiki_mcp.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
