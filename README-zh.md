# Repository DeepWiki 仓库知识助手

[中文](README-zh.md) | [English](README.md)

这个仓库提供三个可安装的源码仓库知识助手：

- `hugegraph-deepwiki-skill`：面向 [apache/hugegraph](https://github.com/apache/hugegraph) 的问答助手
- `hugegraph-ai-deepwiki-skill`：面向 [apache/hugegraph-ai](https://github.com/apache/hugegraph-ai) 的问答助手
- `seatunnel-deepwiki-skill`：面向 [apache/seatunnel](https://github.com/apache/seatunnel) 的问答助手

重点是让 Claude Code 和 Codex 能快速回答这些源码仓库相关的问题，包括架构、模块、API、配置、工作流、示例和实现细节。

DeepWiki 是底层知识查询和 MCP 传输通道。这些 skill 都会调用官方 DeepWiki MCP endpoint：

```text
https://mcp.deepwiki.com/mcp
```

## 运行方式

日常问答不会 clone 上游仓库到本地检索，而是使用线上 DeepWiki + 本地缓存的方式：

1. 本地没有缓存时，对目标仓库调用一次 DeepWiki `read_wiki_contents`。
2. 将 DeepWiki 生成的 wiki 快照保存到用户缓存目录，优先使用 `DEEPWIKI_MCP_CACHE_DIR`，其次是 `XDG_CACHE_HOME`，最后是 `~/.cache/deepwiki-mcp`。
3. 后续问题优先在本地缓存的 wiki 中检索，只把相关片段交给 Claude Code 或 Codex。
4. 当缓存内容找不到精准答案时，调用 DeepWiki `ask_question` 获取线上答案。

`ask_question` 通常返回最终答案、推荐 wiki 页面或 DeepWiki search 链接。需要参考文件时，使用 `context` 命令返回的缓存 wiki 片段；这些片段在 DeepWiki 可用时会包含页面级 source references。

为了得到准确的线上答案，agent 应该把用户原始问题直接传给 `ask_question`，不要扩写成长提示词。普通问答不应 clone 上游仓库；如果确实需要校验当前源码，优先使用线上源码链接或 GitHub raw 文件。

如果明确需要刷新 DeepWiki 快照，可以在内置脚本命令中加 `--refresh`。

## 仓库结构

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
└── plugins/
    ├── hugegraph-deepwiki-skill/
    │   ├── .claude-plugin/plugin.json
    │   ├── .codex-plugin/plugin.json
    │   └── skills/hugegraph-deepwiki-skill/
    ├── hugegraph-ai-deepwiki-skill/
    │   ├── .claude-plugin/plugin.json
    │   ├── .codex-plugin/plugin.json
    │   └── skills/hugegraph-ai-deepwiki-skill/
    └── seatunnel-deepwiki-skill/
        ├── .claude-plugin/plugin.json
        ├── .codex-plugin/plugin.json
        └── skills/seatunnel-deepwiki-skill/
```

`plugins/` 是标准安装来源。每个 plugin 内部的 `skills/` 目录都是自包含 skill，也可以直接复制到 Claude Code 或 Codex 的用户级 skills 目录。

## Claude Code 安装

从本地 clone 安装：

```bash
git clone <repo-url>
cd <repo-directory>
claude plugin marketplace add "$(pwd)"
claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install seatunnel-deepwiki-skill@hugegraph-deepwiki-skills
```

仓库发布后，也可以从远程仓库添加 marketplace：

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install seatunnel-deepwiki-skill@hugegraph-deepwiki-skills
```

如果只想在一次 Claude Code 会话里临时使用：

```bash
claude --plugin-dir ./plugins/hugegraph-deepwiki-skill
claude --plugin-dir ./plugins/hugegraph-ai-deepwiki-skill
claude --plugin-dir ./plugins/seatunnel-deepwiki-skill
```

### 让 Claude Code 自动安装

在任意 Claude Code 工作区粘贴下面这段：

```text
Clone <repo-url>, enter the cloned repository, run `claude plugin marketplace add "$(pwd)"`, then install `hugegraph-deepwiki-skill@hugegraph-deepwiki-skills`, `hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`, and `seatunnel-deepwiki-skill@hugegraph-deepwiki-skills`. Do not hardcode local absolute paths; use the cloned repository path.
```

如果当前已经打开这个仓库，可以粘贴：

```text
Install the three Claude Code plugins from the current repository by running `claude plugin marketplace add "$(pwd)"`, then `claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills`, `claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`, and `claude plugin install seatunnel-deepwiki-skill@hugegraph-deepwiki-skills`.
```

## Codex 安装

从本地 clone 安装：

```bash
git clone <repo-url>
cd <repo-directory>
codex plugin marketplace add "$(pwd)"
codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add seatunnel-deepwiki-skill@hugegraph-deepwiki-skills
```

仓库发布后，也可以从远程仓库添加 marketplace：

```bash
codex plugin marketplace add <owner>/<repo> --ref main
codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add seatunnel-deepwiki-skill@hugegraph-deepwiki-skills
```

Codex plugin manifest 位于：

```text
.agents/plugins/marketplace.json
plugins/hugegraph-deepwiki-skill/.codex-plugin/plugin.json
plugins/hugegraph-ai-deepwiki-skill/.codex-plugin/plugin.json
plugins/seatunnel-deepwiki-skill/.codex-plugin/plugin.json
```

`.agents/plugins/marketplace.json` 是仓库级 Codex marketplace manifest。每个 plugin 内部也有自己的 `.codex-plugin/plugin.json`。

部分旧版 Codex 可能只有 marketplace 注册命令，没有直接安装 plugin 的命令。这种情况下可以手动安装 raw skills：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/seatunnel-deepwiki-skill/skills/seatunnel-deepwiki-skill "$CODEX_HOME/skills/"
```

### 让 Codex 自动安装

在任意 Codex 工作区粘贴下面这段：

```text
Clone <repo-url>, enter the cloned repository, run `codex plugin marketplace add "$(pwd)"`, then install `hugegraph-deepwiki-skill@hugegraph-deepwiki-skills`, `hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`, and `seatunnel-deepwiki-skill@hugegraph-deepwiki-skills` with `codex plugin add`. If this Codex build has no plugin add command, copy the skill folders under `plugins/*/skills/` into `${CODEX_HOME:-$HOME/.codex}/skills`. Do not hardcode local absolute paths.
```

如果当前已经打开这个仓库，可以粘贴：

```text
Install the three Codex skills from the current repository. First run `codex plugin marketplace add "$(pwd)"`, then run `codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills`, `codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`, and `codex plugin add seatunnel-deepwiki-skill@hugegraph-deepwiki-skills`. If this environment has no plugin add command, copy the skill folders under `plugins/*/skills/` into `${CODEX_HOME:-$HOME/.codex}/skills`.
```

## 手动安装 Skill

Claude Code 用户级 skills：

```bash
mkdir -p ~/.claude/skills
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill ~/.claude/skills/
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill ~/.claude/skills/
cp -R plugins/seatunnel-deepwiki-skill/skills/seatunnel-deepwiki-skill ~/.claude/skills/
```

Codex 用户级 skills：

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/seatunnel-deepwiki-skill/skills/seatunnel-deepwiki-skill "$CODEX_HOME/skills/"
```

## 使用方式

安装后，可以在提问时显式指定对应 skill：

```text
Use $hugegraph-deepwiki-skill to explain HugeGraph schema and traversal behavior.
```

```text
Use $hugegraph-ai-deepwiki-skill to explain the HugeGraph AI RAG workflow.
```

```text
Use $seatunnel-deepwiki-skill to explain how SeaTunnel loads connectors.
```

HugeGraph 数据库相关问题使用 `hugegraph-deepwiki-skill`，HugeGraph AI/RAG 相关问题使用 `hugegraph-ai-deepwiki-skill`，SeaTunnel 数据集成相关问题使用 `seatunnel-deepwiki-skill`。三个助手保持独立，避免回答时混用源码仓库上下文。
