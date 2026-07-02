---
name: hugegraph-ai-deepwiki-skill
description: "Use when users ask about Apache HugeGraph AI or apache/hugegraph-ai source code, architecture, modules, examples, agents, RAG workflows, graph-enhanced AI features, model integration, configuration, installation, demos, or implementation details."
metadata:
  short-description: Apache HugeGraph AI repository assistant
---

# HugeGraph AI Repository Knowledge Assistant

Answer questions about the Apache HugeGraph AI source repository. Use the official DeepWiki MCP server as the underlying knowledge retrieval channel.

- Source repository: `https://github.com/apache/hugegraph-ai`
- DeepWiki page: `https://deepwiki.com/apache/hugegraph-ai`
- MCP endpoint: `https://mcp.deepwiki.com/mcp`
- Default repository: `apache/hugegraph-ai`

## 触发条件

| 场景 | 典型输入 | 处理方式 |
| --- | --- | --- |
| MUST 触发 | 询问 HugeGraph AI 源码、架构、模块、Agent、RAG、图增强 AI、模型集成、配置或示例 | 先运行 `context` 检索 DeepWiki 缓存；不足时运行 `ask` |
| SHOULD 触发 | 询问 HugeGraph AI demo、安装步骤、provider 配置、文本转 Gremlin 或 graph RAG 实现位置 | 可先运行 `structure` 定位，再用 `context` 或 `ask` |
| MUST NOT 触发 | 询问 HugeGraph Core、非 HugeGraph AI 项目、纯通用 LLM/RAG 概念且无需仓库事实 | 使用更匹配的 skill 或普通回答 |

## 工作流程

```text
┌──────────────┐
│ User question│
└──────┬───────┘
       │
       v
┌──────────────────────┐
│ context: local cache  │
└──────┬───────────────┘
       │ direct answer?
   yes │ no
       v
┌──────────────┐    ┌──────────────────────┐
│ answer user  │    │ ask: online DeepWiki  │
└──────────────┘    └──────────┬───────────┘
                               v
                        ┌──────────────┐
                        │ answer user  │
                        └──────────────┘
```

## Default Workflow

1. Preserve the user's question, including code snippets, version constraints, error messages, model/provider details, and environment details.
2. Change directory to this skill directory, the directory containing this `SKILL.md`.
3. Search the local DeepWiki wiki cache for relevant context. If the cache does not exist yet, this command fetches `read_wiki_contents` from DeepWiki once and saves it under the user's cache directory. It prints only relevant snippets, not the full wiki dump:

```bash
python3 scripts/deepwiki_mcp.py context --repo hugegraph-ai --query "<user question>"
```

4. Answer from cached context only when the snippets directly and precisely answer the user's question. If they are merely related background, continue to `ask`.
5. For broad navigation questions, read the wiki structure instead:

```bash
python3 scripts/deepwiki_mcp.py structure --repo hugegraph-ai
```

6. If the cached wiki context does not directly and precisely answer the question, do not answer the user yet. You must use DeepWiki's AI `ask_question` tool to request an online answer:

```bash
python3 scripts/deepwiki_mcp.py ask --repo hugegraph-ai --question "<user question>"
```

7. For `ask`, preserve the user's original question. Do not expand it with extra requirements, long source-reference requests, or your own multi-part prompt; longer generated questions are more likely to time out.
8. If `ask` returns uncertainty, times out, or reports a transport/query error, retry once with the shortest faithful form of the user's original question. If it still fails, say so plainly and answer only from the cached context if it is sufficient.
9. If the user needs source references for an `ask` answer, use the cached context or contents to identify the relevant wiki page snippets and source-file references. `ask` usually returns the final answer plus suggested wiki pages or a DeepWiki search link, not the raw code files used to generate the answer.

## Routing Rules

- Use `structure` first for navigation, table-of-contents, onboarding, or "where should I start?" questions.
- Use `context` first for normal Q&A, source-reference requests, and token-efficient grounding.
- Use `ask` after `context` whenever cached snippets do not provide a direct and precise answer, or when the question needs synthesis across multiple areas. Do not answer directly from related-but-insufficient cached snippets.
- If both an online answer and source references are needed, run `ask` for the answer and use `context` to collect source references.
- Do not clone the repository for ordinary Q&A or verification. If current source verification is truly required, prefer online source links or raw GitHub files and clearly distinguish that from DeepWiki-grounded content.

## 使用方法

- 在 skill 根目录运行命令；所有脚本和引用文件均使用相对路径。
- 普通问答优先运行 `python3 scripts/deepwiki_mcp.py context --repo hugegraph-ai --query "<question>"`。
- 缓存片段不能直接回答时，再运行 `python3 scripts/deepwiki_mcp.py ask --repo hugegraph-ai --question "<question>"`。
- 如需刷新 DeepWiki 预处理内容，仅在用户明确要求时给 `contents` 或 `context` 加 `--refresh`。

## 使用示例

```bash
python3 scripts/deepwiki_mcp.py context --repo hugegraph-ai --query "How does HugeGraph AI implement graph RAG?"
python3 scripts/deepwiki_mcp.py ask --repo hugegraph-ai --question "Where are LLM providers configured in HugeGraph AI?"
python3 scripts/deepwiki_mcp.py structure --repo hugegraph-ai
```

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

The `contents` command uses the same local cache by default. Use `--refresh` only when the user explicitly needs a fresh DeepWiki snapshot.

For normal Q&A, prefer `context` over `contents` so only the relevant cached snippets enter the model context. When the cached wiki context does not directly and precisely answer the question, run `ask` for an online DeepWiki answer before responding.

## Repository Profile

The repository alias lives in `references/repos.json`.

- `hugegraph-ai` maps to `apache/hugegraph-ai`.
- For Apache HugeGraph core graph database questions, use the separate `hugegraph-deepwiki-skill` instead of this skill.

## Answering Guidance

- Optimize answers for newcomers: explain the relevant concept, name the module or example to inspect next, and give a short next step when DeepWiki provides one.
- Keep responses practical: include class/module names, configuration keys, scripts, commands, or example paths when DeepWiki provides them.
- Prefer online DeepWiki retrieval and cached wiki search. Do not clone the source repository just to answer a question.
- If the user asks for code changes in a local HugeGraph AI checkout, use DeepWiki for orientation, then inspect and edit the local repository directly.
- Do not invent details that DeepWiki does not provide. Clearly distinguish DeepWiki-grounded facts from your own inference.
- For version-sensitive release, dependency, provider, or API-compatibility questions, verify with the live repository or official docs when the user needs current facts beyond the DeepWiki answer.

## 错误处理

- If `context` returns no precise snippet, run `ask` before answering.
- If `ask` times out, retry once with the shortest faithful form of the original question.
- If DeepWiki or the network is unavailable, say that retrieval failed and answer only when cached snippets are sufficient.
- If Python is missing, install Python 3.9+ or run on an environment that provides it.
