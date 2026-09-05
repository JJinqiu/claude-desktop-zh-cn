# Claude Desktop 中文补丁 AI 协作入口

处理本项目时，AI 助手应先读取以下知识库入口。所有路径以本项目根目录为基准；本项目与 `AIKnowledgeVault` 采用同级 checkout 布局。

1. [知识库总说明](../AIKnowledgeVault/README.md)
2. [维护协议](../AIKnowledgeVault/AI项目维护协议.md)
3. [项目索引](<../AIKnowledgeVault/80 Index/Project Index.md>)
4. [Claude Desktop 中文补丁项目档案](<../AIKnowledgeVault/20 Projects/Claude Desktop 中文补丁/项目主页.md>)

如果相对路径无法解析，应先确认知识库挂载位置；不要回退到其他机器的旧绝对路径。

## 文档边界

- 本工作目录负责代码、脚本、资源文件和本地验证。
- 长期项目上下文写入 `AIKnowledgeVault\20 Projects\Claude Desktop 中文补丁\`。
- 更新后重新汉化流程写入 `AIKnowledgeVault\40 Workflows\Claude Desktop 中文补丁\`。
- 如果形成明确方案取舍，再写入 `AIKnowledgeVault\60 Decisions\Claude Desktop 中文补丁\`。

## 常用验证

```powershell
python tests/validate_zh_cn.py
python -m json.tool resources/frontend-zh-CN.json > $null
```

Claude 自动更新后，先按[重新汉化工作流](<../AIKnowledgeVault/40 Workflows/Claude Desktop 中文补丁/Claude Desktop 更新后重新汉化流程.md>)核对平台、源码版本、资源和失败处理。校验失败立即停止安装；文档验证不等于当前应用版本安装成功。
