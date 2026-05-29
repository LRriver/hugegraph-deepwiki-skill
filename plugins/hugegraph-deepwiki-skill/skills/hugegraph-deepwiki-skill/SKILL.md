---
name: hugegraph-deepwiki-skill
description: Use this skill as a repository knowledge assistant for Apache HugeGraph, apache/hugegraph source code, architecture, modules, APIs, configuration, storage backends, Gremlin/traversal behavior, schema/modeling, server/client tooling, build/test workflows, or implementation details. It answers questions grounded in apache/hugegraph and uses the official DeepWiki MCP wiki as the underlying retrieval channel.
metadata:
  short-description: Apache HugeGraph repository assistant
---

# HugeGraph Repository Knowledge Assistant

Answer questions about the Apache HugeGraph source repository. Use the official DeepWiki MCP server as the underlying knowledge retrieval channel.

- Source repository: `https://github.com/apache/hugegraph`
- DeepWiki page: `https://deepwiki.com/apache/hugegraph`
- MCP endpoint: `https://mcp.deepwiki.com/mcp`
- Default repository: `apache/hugegraph`

## Default Workflow

1. Preserve the user's question, including code snippets, version constraints, error messages, and environment details.
2. Change directory to this skill directory, the directory containing this `SKILL.md`.
3. For reliable repository-grounded answers, read the wiki contents and synthesize the answer:

```bash
python3 scripts/deepwiki_mcp.py contents --repo hugegraph
```

4. For broad navigation questions, read the wiki structure instead:

```bash
python3 scripts/deepwiki_mcp.py structure --repo hugegraph
```

5. Use DeepWiki's AI `ask_question` tool only when a direct synthesis from contents is insufficient:

```bash
python3 scripts/deepwiki_mcp.py ask --repo hugegraph --question "<user question>"
```

6. Answer the user in your own words using the repository-grounded result as the primary source. Mention that DeepWiki MCP was used as the retrieval channel when that provenance is helpful.
7. If `ask` returns uncertainty, times out, or reports a transport/query error, fall back to `contents` and synthesize from the wiki text.

## When to Read Structure or Pages

For broad navigation questions, or when the user asks where something lives, inspect the wiki structure:

```bash
cd <directory-containing-this-SKILL.md>
python3 scripts/deepwiki_mcp.py structure --repo hugegraph
```

If the user needs a fuller wiki dump for offline review or synthesis, read the wiki contents:

```bash
cd <directory-containing-this-SKILL.md>
python3 scripts/deepwiki_mcp.py contents --repo hugegraph
```

Then synthesize the final answer from the retrieved wiki text. Keep `ask` as an optional fallback only when the wiki contents do not provide enough context.

## Repository Profile

The repository alias lives in `references/repos.json`.

- `hugegraph` maps to `apache/hugegraph`.
- For Apache HugeGraph AI questions, use the separate `hugegraph-ai-deepwiki-skill` instead of this skill.

## Answering Guidance

- Keep responses practical: include class/module names, configuration keys, command names, or API names when DeepWiki provides them.
- If the user asks for code changes in a local HugeGraph checkout, use DeepWiki for orientation, then inspect and edit the local repository directly.
- Do not invent details that DeepWiki does not provide. Clearly distinguish DeepWiki-grounded facts from your own inference.
- For version-sensitive release, dependency, or API-compatibility questions, verify with the live repository or official docs when the user needs current facts beyond the DeepWiki answer.
