---
name: hugegraph-deepwiki-skill
description: Use this skill when answering questions about Apache HugeGraph, apache/hugegraph source code, architecture, modules, APIs, configuration, storage backends, Gremlin/traversal behavior, schema/modeling, server/client tooling, build/test workflows, or implementation details. The skill forwards the user's question to the official DeepWiki MCP wiki for apache/hugegraph and returns the answer grounded in that repository.
metadata:
  short-description: Ask DeepWiki about Apache HugeGraph
---

# HugeGraph DeepWiki

Use the official DeepWiki MCP server to answer questions about Apache HugeGraph.

- DeepWiki page: `https://deepwiki.com/apache/hugegraph`
- MCP endpoint: `https://mcp.deepwiki.com/mcp`
- Default repository: `apache/hugegraph`

## Default Workflow

1. Preserve the user's question, including code snippets, version constraints, error messages, and environment details.
2. Ask DeepWiki with the bundled client:

```bash
python3 scripts/deepwiki_mcp.py ask --repo hugegraph --question "<user question>"
```

3. Answer the user in your own words using DeepWiki's result as the primary source. Mention that the answer comes from the HugeGraph DeepWiki when that provenance is helpful.
4. If DeepWiki returns uncertainty, missing coverage, or a transport error, say so plainly and ask for the smallest useful follow-up detail.

## When to Read Structure or Pages

For broad navigation questions, or when the user asks where something lives, inspect the wiki structure:

```bash
python3 scripts/deepwiki_mcp.py structure --repo hugegraph
```

If the user needs a fuller wiki dump for offline review or synthesis, read the wiki contents:

```bash
python3 scripts/deepwiki_mcp.py contents --repo hugegraph
```

Then synthesize the final answer. Prefer `ask` for normal Q&A; use `structure` and `contents` only when they add useful grounding.

## Repository Profile

The repository alias lives in `references/repos.json`.

- `hugegraph` maps to `apache/hugegraph`.
- For Apache HugeGraph AI questions, use the separate `hugegraph-ai-deepwiki-skill` instead of this skill.

## Answering Guidance

- Keep responses practical: include class/module names, configuration keys, command names, or API names when DeepWiki provides them.
- If the user asks for code changes in a local HugeGraph checkout, use DeepWiki for orientation, then inspect and edit the local repository directly.
- Do not invent details that DeepWiki does not provide. Clearly distinguish DeepWiki-grounded facts from your own inference.
- For version-sensitive release, dependency, or API-compatibility questions, verify with the live repository or official docs when the user needs current facts beyond the DeepWiki answer.
