# Contributing / 贡献指南

欢迎改进命名体验、项目选择、历史覆盖检查和数据库兼容性。

## 本地开发

1. Fork 并克隆仓库，创建工作分支。
2. 修改 skill 规则时同步检查 `agents/openai.yaml` 与中英文 README。
3. 修改脚本时添加能够说明行为的测试，使用临时合成数据。
4. 运行 `python3 -m unittest discover -s tests -v`。
5. 提交 PR，说明问题、变化及验证范围。

请保持项目由用户选择、预览不写入、数据库只读、应用 API 修改标题等约束。摘要阅读不能声称已通读全文；缺少应用工具时不能声称实际改名成功。

Issue 中请提供预期行为、实际结果、Python 版本及脱敏后的最小复现。不要上传真实聊天历史、数据库、访问令牌或个人路径。数据库兼容问题优先提供字段名称及合成样例。

## English

Fork the repository, create a branch, and describe the problem and validation in your PR. Keep both READMEs and skill metadata consistent. Use synthetic temporary databases for tests and run `python3 -m unittest discover -s tests -v`.

Preserve explicit project selection, preview-only behavior, read-only database access, and application-based title writes. Never submit real chat histories, databases, tokens, or private paths in issues or test fixtures.
