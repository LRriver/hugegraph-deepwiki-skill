---
name: hugegraph-ai-deepwiki-skill
description: Use this skill as a repository knowledge assistant for Apache HugeGraph AI, apache/hugegraph-ai source code, architecture, modules, examples, agents, RAG workflows, graph-enhanced AI features, model integration, configuration, installation, demos, or implementation details. It answers questions grounded in apache/hugegraph-ai and uses the official DeepWiki MCP wiki as the underlying retrieval channel.
metadata:
  short-description: Apache HugeGraph AI repository assistant
---

# HugeGraph AI Repository Knowledge Assistant

Answer questions about the Apache HugeGraph AI source repository. Use the official DeepWiki MCP server as the underlying knowledge retrieval channel.

- Source repository: `https://github.com/apache/hugegraph-ai`
- DeepWiki page: `https://deepwiki.com/apache/hugegraph-ai`
- MCP endpoint: `https://mcp.deepwiki.com/mcp`
- Default repository: `apache/hugegraph-ai`

## Default Workflow

1. Preserve the user's question, including code snippets, version constraints, error messages, model/provider details, and environment details.
2. Change directory to this skill directory, the directory containing this `SKILL.md`.
3. For reliable repository-grounded answers, read the wiki contents and synthesize the answer:

```bash
python3 scripts/deepwiki_mcp.py contents --repo hugegraph-ai
```

4. For broad navigation questions, read the wiki structure instead:

```bash
python3 scripts/deepwiki_mcp.py structure --repo hugegraph-ai
```

5. Use DeepWiki's AI `ask_question` tool only when a direct synthesis from contents is insufficient:

```bash
python3 scripts/deepwiki_mcp.py ask --repo hugegraph-ai --question "<user question>"
```

6. Answer the user in your own words using the repository-grounded result as the primary source. Mention that DeepWiki MCP was used as the retrieval channel when that provenance is helpful.
7. If `ask` returns uncertainty, times out, or reports a transport/query error, fall back to `contents` and synthesize from the wiki text.

## When to Read Structure or Contents

For broad orientation questions, onboarding questions, or "where should I start?" prompts, inspect the wiki structure:

```bash
cd <directory-containing-this-SKILL.md>
python3 scripts/deepwiki_mcp.py structure --repo hugegraph-ai
```

If the user needs a fuller wiki dump for offline review or synthesis, read the wiki contents:

```bash
cd <directory-containing-this-SKILL.md>
python3 scripts/deepwiki_mcp.py contents --repo hugegraph-ai
```

Then synthesize the final answer from the retrieved wiki text. Keep `ask` as an optional fallback only when the wiki contents do not provide enough context.

## Repository Profile

The repository alias lives in `references/repos.json`.

- `hugegraph-ai` maps to `apache/hugegraph-ai`.
- For Apache HugeGraph core graph database questions, use the separate `hugegraph-deepwiki-skill` instead of this skill.

## Answering Guidance

- Optimize answers for newcomers: explain the relevant concept, name the module or example to inspect next, and give a short next step when DeepWiki provides one.
- Keep responses practical: include class/module names, configuration keys, scripts, commands, or example paths when DeepWiki provides them.
- If the user asks for code changes in a local HugeGraph AI checkout, use DeepWiki for orientation, then inspect and edit the local repository directly.
- Do not invent details that DeepWiki does not provide. Clearly distinguish DeepWiki-grounded facts from your own inference.
- For version-sensitive release, dependency, provider, or API-compatibility questions, verify with the live repository or official docs when the user needs current facts beyond the DeepWiki answer.
