---
name: hugegraph-ai-deepwiki-skill
description: Use this skill when answering questions about Apache HugeGraph AI, apache/hugegraph-ai source code, architecture, modules, examples, agents, RAG workflows, graph-enhanced AI features, model integration, configuration, installation, demos, or implementation details. The skill forwards the user's question to the official DeepWiki MCP wiki for apache/hugegraph-ai and returns the answer grounded in that repository.
metadata:
  short-description: Ask DeepWiki about Apache HugeGraph AI
---

# HugeGraph AI DeepWiki

Use the official DeepWiki MCP server to answer questions about Apache HugeGraph AI.

- DeepWiki page: `https://deepwiki.com/apache/hugegraph-ai`
- MCP endpoint: `https://mcp.deepwiki.com/mcp`
- Default repository: `apache/hugegraph-ai`

## Default Workflow

1. Preserve the user's question, including code snippets, version constraints, error messages, model/provider details, and environment details.
2. Ask DeepWiki with the bundled client:

```bash
python3 scripts/deepwiki_mcp.py ask --repo hugegraph-ai --question "<user question>"
```

3. Answer the user in your own words using DeepWiki's result as the primary source. Mention that the answer comes from the HugeGraph AI DeepWiki when that provenance is helpful.
4. If DeepWiki returns uncertainty, missing coverage, or a transport error, say so plainly and ask for the smallest useful follow-up detail.

## When to Read Structure or Contents

For broad orientation questions, onboarding questions, or "where should I start?" prompts, inspect the wiki structure:

```bash
python3 scripts/deepwiki_mcp.py structure --repo hugegraph-ai
```

If the user needs a fuller wiki dump for offline review or synthesis, read the wiki contents:

```bash
python3 scripts/deepwiki_mcp.py contents --repo hugegraph-ai
```

Then synthesize the final answer. Prefer `ask` for normal Q&A; use `structure` and `contents` only when they add useful grounding.

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
