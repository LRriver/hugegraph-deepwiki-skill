# 功能简介

HugeGraph Repository Assistant 是面向 Apache HugeGraph 源码仓库的知识问答技能。它基于 DeepWiki MCP 获取 `apache/hugegraph` 的预处理仓库知识，优先使用本地缓存检索相关片段，在缓存无法精准回答时再调用 DeepWiki 在线问答。

**适用场景**

- 了解 Apache HugeGraph 的源码结构、模块职责、核心 API、配置项和构建测试流程。
- 查询 Gremlin/traversal、schema/modeling、存储后端、server/client 工具等实现细节。
- 在修改 HugeGraph 代码前快速定位相关类、模块、配置或文档页面。

**不适用场景**

- 不适合回答 HugeGraph AI 仓库问题；这类问题应使用 HugeGraph AI Repository Assistant。
- 不适合完全离线使用；首次建立缓存和在线 `ask` 都需要访问 DeepWiki MCP。
- 不适合作为实时源码审计工具；需要最新代码事实时仍应核对 GitHub 或本地仓库。

**依赖要求**

- Python 3.9+。
- 当前环境可以访问 `https://mcp.deepwiki.com/mcp`。
- 云平台运行环境允许写入缓存目录；如默认 home 不可写，可设置 `DEEPWIKI_MCP_CACHE_DIR=/tmp/deepwiki-mcp`。

# **快速开始**

上传技能 ZIP 后，在会话中直接提出 Apache HugeGraph 仓库相关问题，例如：

```text
HugeGraph 的 RocksDB backend 配置在哪里处理？
```

技能会先搜索本地 DeepWiki 缓存；如果缓存中没有精准答案，会继续请求 DeepWiki 在线问答。

# 使用方式

• 输入格式：自然语言问题，建议包含模块名、类名、配置项、错误信息或版本背景。

• 输出示例：说明相关模块或类的职责，给出可继续查看的文件/配置/API 名称，并标明结论来自 DeepWiki 缓存或在线问答。

# 故障排除

- 如果提示无法访问 DeepWiki MCP，请检查网络或代理配置。
- 如果缓存目录不可写，请设置 `DEEPWIKI_MCP_CACHE_DIR` 到可写目录。
- 如果回答不够精准，请补充类名、模块名、配置项或错误日志后重试。

# 经典案例

- “HugeGraph schema 校验逻辑在哪里？”
- “Gremlin 查询在 server 侧如何进入执行流程？”
- “RocksDB backend 相关配置项有哪些？”
- “HugeGraph client 和 server 的构建测试入口是什么？”
