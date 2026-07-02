# 功能简介

SeaTunnel Repository Assistant 是面向 Apache SeaTunnel 源码仓库的知识问答技能。它基于 DeepWiki MCP 获取 `apache/seatunnel` 的预处理仓库知识，优先使用本地缓存检索相关片段，在缓存无法精准回答时再调用 DeepWiki 在线问答。

**适用场景**

- 了解 Apache SeaTunnel 的源码结构、模块职责、connector、engine、job、配置和构建测试流程。
- 查询连接器加载、任务配置解析、部署运行、插件开发、数据同步流程等实现细节。
- 在修改 SeaTunnel 代码前快速定位相关类、模块、配置或文档页面。

**不适用场景**

- 不适合回答非 SeaTunnel 仓库问题；这类问题应使用对应仓库的知识助手。
- 不适合完全离线使用；首次建立缓存和在线 `ask` 都需要访问 DeepWiki MCP。
- 不适合作为实时源码审计工具；需要最新代码事实时仍应核对 GitHub 或本地仓库。

**依赖要求**

- Python 3.9+。
- 当前环境可以访问 `https://mcp.deepwiki.com/mcp`。
- 云平台运行环境允许写入缓存目录；如默认 home 不可写，可设置 `DEEPWIKI_MCP_CACHE_DIR=/tmp/deepwiki-mcp`。

# **快速开始**

上传技能 ZIP 后，在会话中直接提出 Apache SeaTunnel 仓库相关问题，例如：

```text
SeaTunnel 的 connector 是怎么加载的？
```

技能会先搜索本地 DeepWiki 缓存；如果缓存中没有精准答案，会继续请求 DeepWiki 在线问答。

# 使用方式

• 输入格式：自然语言问题，建议包含模块名、connector 名、engine 名、配置项、错误信息或版本背景。

• 输出示例：说明相关模块或类的职责，给出可继续查看的文件/配置/API 名称，并标明结论来自 DeepWiki 缓存或在线问答。

# 故障排除

- 如果提示无法访问 DeepWiki MCP，请检查网络或代理配置。
- 如果缓存目录不可写，请设置 `DEEPWIKI_MCP_CACHE_DIR` 到可写目录。
- 如果回答不够精准，请补充类名、模块名、connector 名、配置项或错误日志后重试。

# 经典案例

- “SeaTunnel connector 加载流程在哪里？”
- “SeaTunnel job 配置是在哪个模块解析的？”
- “SeaTunnel 支持哪些 engine，入口在哪里？”
- “如何定位某个 source/sink connector 的实现？”
