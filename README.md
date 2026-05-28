# HugeGraph Repository Knowledge Assistants

[中文](README-zh.md) | [English](README.md)

This repository provides two installable repository knowledge assistants for the Apache HugeGraph project family:

- `hugegraph-deepwiki-skill`: Q&A assistant for [apache/hugegraph](https://github.com/apache/hugegraph)
- `hugegraph-ai-deepwiki-skill`: Q&A assistant for [apache/hugegraph-ai](https://github.com/apache/hugegraph-ai)

The goal is to help Claude Code and Codex answer questions about the two source repositories quickly: architecture, modules, APIs, configuration, workflows, examples, and implementation details.

DeepWiki is the underlying knowledge and MCP transport layer used by these assistants. Both skills call the official DeepWiki MCP endpoint:

```text
https://mcp.deepwiki.com/mcp
```

## Repository Layout

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
└── plugins/
    ├── hugegraph-deepwiki-skill/
    │   ├── .claude-plugin/plugin.json
    │   ├── .codex-plugin/plugin.json
    │   └── skills/hugegraph-deepwiki-skill/
    └── hugegraph-ai-deepwiki-skill/
        ├── .claude-plugin/plugin.json
        ├── .codex-plugin/plugin.json
        └── skills/hugegraph-ai-deepwiki-skill/
```

`plugins/` is the canonical install source. The skill folders inside each plugin are self-contained and can also be copied directly into Claude Code or Codex skill directories.

## Claude Code Install

From a local clone:

```bash
git clone <repo-url>
cd <repo-directory>
claude plugin marketplace add "$(pwd)"
claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
```

After the repository is published, Claude Code can add the marketplace from the remote Git repository:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
```

For one-session use without installing globally:

```bash
claude --plugin-dir ./plugins/hugegraph-deepwiki-skill
claude --plugin-dir ./plugins/hugegraph-ai-deepwiki-skill
```

### Ask Claude Code To Install It

Paste this into Claude Code from any workspace:

```text
Clone <repo-url>, enter the cloned repository, run `claude plugin marketplace add "$(pwd)"`, then install `hugegraph-deepwiki-skill@hugegraph-deepwiki-skills` and `hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`. Do not hardcode local absolute paths; use the cloned repository path.
```

If the repository is already open in Claude Code, use:

```text
Install the two Claude Code plugins from the current repository by running `claude plugin marketplace add "$(pwd)"`, then `claude plugin install hugegraph-deepwiki-skill@hugegraph-deepwiki-skills` and `claude plugin install hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`.
```

## Codex Install

From a local clone:

```bash
git clone <repo-url>
cd <repo-directory>
codex plugin marketplace add "$(pwd)"
codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
```

After the repository is published, Codex can add the marketplace from the remote Git repository:

```bash
codex plugin marketplace add <owner>/<repo> --ref main
codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills
codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills
```

This repository includes Codex plugin manifests at:

```text
.agents/plugins/marketplace.json
plugins/hugegraph-deepwiki-skill/.codex-plugin/plugin.json
plugins/hugegraph-ai-deepwiki-skill/.codex-plugin/plugin.json
```

`.agents/plugins/marketplace.json` is the repository-level Codex marketplace manifest. Each plugin also has its own `.codex-plugin/plugin.json`.

Older Codex builds may expose marketplace registration but not a direct plugin install command. In that case, install the raw skills manually:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill "$CODEX_HOME/skills/"
```

### Ask Codex To Install It

Paste this into Codex from any workspace:

```text
Clone <repo-url>, enter the cloned repository, run `codex plugin marketplace add "$(pwd)"`, then install `hugegraph-deepwiki-skill@hugegraph-deepwiki-skills` and `hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills` with `codex plugin add`. If this Codex build has no plugin add command, copy `plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill` and `plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill` into `${CODEX_HOME:-$HOME/.codex}/skills`. Do not hardcode local absolute paths.
```

If the repository is already open in Codex, use:

```text
Install the two Codex skills from the current repository. First run `codex plugin marketplace add "$(pwd)"`, then run `codex plugin add hugegraph-deepwiki-skill@hugegraph-deepwiki-skills` and `codex plugin add hugegraph-ai-deepwiki-skill@hugegraph-deepwiki-skills`. If this environment has no plugin add command, copy the two skill folders under `plugins/*/skills/` into `${CODEX_HOME:-$HOME/.codex}/skills`.
```

## Manual Skill Install

Claude Code user-level skills:

```bash
mkdir -p ~/.claude/skills
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill ~/.claude/skills/
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill ~/.claude/skills/
```

Codex user-level skills:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
cp -R plugins/hugegraph-deepwiki-skill/skills/hugegraph-deepwiki-skill "$CODEX_HOME/skills/"
cp -R plugins/hugegraph-ai-deepwiki-skill/skills/hugegraph-ai-deepwiki-skill "$CODEX_HOME/skills/"
```

## Usage

After installation, ask for the relevant skill explicitly when needed:

```text
Use $hugegraph-deepwiki-skill to explain HugeGraph schema and traversal behavior.
```

```text
Use $hugegraph-ai-deepwiki-skill to explain the HugeGraph AI RAG workflow.
```

Use the HugeGraph assistant for the graph database repository and the HugeGraph AI assistant for the AI/RAG repository. Keep the two separate so answers stay grounded in the intended source repository.
