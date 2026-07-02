# 功能简介

HugeGraph AI Repository Assistant 是面向 Apache HugeGraph AI 源码仓库的知识问答技能。它基于 DeepWiki MCP 获取 `apache/hugegraph-ai` 的预处理仓库知识，优先使用本地缓存检索相关片段，在缓存无法精准回答时再调用 DeepWiki 在线问答。

**适用场景**

- 了解 HugeGraph AI 的模块结构、Agent、RAG 工作流、图增强 AI 能力和示例。
- 查询模型 provider 配置、文本转 Gremlin、graph RAG、demo 和安装使用细节。
- 在修改 HugeGraph AI 代码前快速定位相关类、脚本、配置或示例路径。

**不适用场景**

- 不适合回答 HugeGraph Core 数据库仓库问题；这类问题应使用 HugeGraph Repository Assistant。
- 不适合完全离线使用；首次建立缓存和在线 `ask` 都需要访问 DeepWiki MCP。
- 不适合作为实时依赖版本查询工具；需要最新事实时仍应核对 GitHub、PyPI 或官方文档。

**依赖要求**

- Python 3.9+。
- 当前环境可以访问 `https://mcp.deepwiki.com/mcp`。
- 云平台运行环境允许写入缓存目录；如默认 home 不可写，可设置 `DEEPWIKI_MCP_CACHE_DIR=/tmp/deepwiki-mcp`。

# **快速开始**

上传技能 ZIP 后，在会话中直接提出 Apache HugeGraph AI 仓库相关问题，例如：

```text
HugeGraph AI 的 graph RAG 流程是怎么实现的？
```

技能会先搜索本地 DeepWiki 缓存；如果缓存中没有精准答案，会继续请求 DeepWiki 在线问答。

# 使用方式

• 输入格式：自然语言问题，建议包含模块名、功能名、模型 provider、示例名、错误信息或版本背景。

• 输出示例：说明相关模块或流程的作用，给出可继续查看的文件/配置/示例名称，并标明结论来自 DeepWiki 缓存或在线问答。

# 故障排除

- 如果提示无法访问 DeepWiki MCP，请检查网络或代理配置。
- 如果缓存目录不可写，请设置 `DEEPWIKI_MCP_CACHE_DIR` 到可写目录。
- 如果回答不够精准，请补充模块名、示例名、配置项或错误日志后重试。

# 经典案例

- “HugeGraph AI 的 RAG pipeline 从哪里开始？”
- “LLM provider 配置在哪些文件里？”
- “text2gremlin 示例如何调用模型？”
- “graph RAG 和普通 RAG 的差异在代码里体现在哪里？”
