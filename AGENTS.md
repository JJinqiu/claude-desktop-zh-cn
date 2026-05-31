# Claude Desktop 中文补丁 AI 协作入口

处理本项目时，AI 助手应先读取知识库项目档案：

```text
D:\Learning\Projects\AIKnowledgeVault\20 Projects\Claude Desktop 中文补丁\项目主页.md
```

同时读取：

```text
D:\Learning\Projects\AIKnowledgeVault\README.md
D:\Learning\Projects\AIKnowledgeVault\AI项目维护协议.md
D:\Learning\Projects\AIKnowledgeVault\80 Index\Project Index.md
```

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

Claude 自动更新后，应先运行校验脚本，再决定是否补新增 key 或直接管理员运行 `install-windows.bat`。
