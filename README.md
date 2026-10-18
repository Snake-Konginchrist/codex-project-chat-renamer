# Codex Project Chat Renamer

按你的选择，清点并重命名 **当前项目、其他项目或多个项目** 的 Codex 对话。

[English](README.en.md) · [使用规则](SKILL.md) · [贡献指南](CONTRIBUTING.md) · [MIT License](LICENSE)

## 能做什么

- 自选项目：当前项目、任意指定项目、多个项目，或指定对话 ID。
- 自选范围：未归档、已归档、用户对话、子代理，以及时间和关键词筛选。
- 自选模式：仅统计、预览方案、直接改名；预览后也可以只执行选中项。
- 自选阅读深度：完整历史、快速摘要、仅规范现有标题。
- 自选命名：前缀、语言、长度、主题风格、自定义模板和重名策略。
- 核验结果：通过应用接口修改并回读标题，记录跳过项、冲突和覆盖缺口。

项目始终由用户决定。未明确项目时会询问，不会仅凭当前工作目录选择目标。

## 环境要求

这是供 Codex 使用的 **skill 指令包**，不是独立的批量改名程序。

完整流程需要运行环境提供项目与对话管理工具：`list_projects`、`list_threads`、`read_thread`、`list_archived_threads` 和 `set_thread_title`。这些工具的可用性取决于应用环境；安装本仓库不会安装或解锁它们。工具不可用时只能交付可支持的盘点或拟定方案，不能声称完成改名。

本地清单补全脚本需要 Python 3.9+，仅使用标准库。它读取当前 host 的 Codex SQLite 状态文件；不能证明远端项目的完整性。

## 安装

在 macOS / Linux 终端中，将仓库克隆到个人 skill 目录：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/Snake-Konginchrist/codex-project-chat-renamer.git ~/.agents/skills/codex-project-chat-renamer
```

如果目标目录已经存在，先检查内容，不要覆盖。Codex 会发现新 skill；未显示时重启应用。目录发现机制见 [OpenAI 官方 skill 文档](https://developers.openai.com/codex/skills)。本仓库以独立 skill 源码形式提供，没有上架插件目录。

## 使用示例

在可使用该 skill 的 Codex 环境中输入：

```text
使用 $codex-project-chat-renamer，让我选择要整理的项目和命名规则，先看预览。
```

```text
使用 $codex-project-chat-renamer，整理项目 Atlas 的未归档用户对话。
通读历史，统一加【Atlas】前缀，后缀最多十字，直接改名，跳过已合规标题。
```

```text
使用 $codex-project-chat-renamer，同时整理 Atlas 和 Beacon 两个项目。
分别使用【Atlas】和【Beacon】前缀，先给我旧名与新名对照，不执行修改。
```

```text
使用 $codex-project-chat-renamer，只统计项目 Beacon 的已归档对话，不改名。
```

仅统计和预览不授权改名。用户已明确要求执行时，不再重复要求确认。

## 选项与默认行为

| 选项 | 默认行为 |
| --- | --- |
| 项目 | 用户选择；未明确时询问 |
| 执行 | 按用户请求；意图不清时预览 |
| 范围 | 所选项目的未归档用户对话 |
| 阅读 | 全文；仅统计无需阅读正文 |
| 标题 | 简洁中文主题，不新增前缀，主题最多 16 个 Unicode 字符 |
| 已有标题 | 跳过符合已明确规则的标题 |
| 重名 | 优先补充区分主题；无法区分则报告 |
| 输出 | 聊天内报告；可要求 JSON / CSV 映射 |

完整选项及执行约束见 [SKILL.md](SKILL.md)。模板支持 `{project}`、`{topic}`、`{action}`、`{module}`、`{date}` 和 `{index}`。

## 单独运行盘点脚本

从本仓库目录运行：

```bash
python3 scripts/inventory.py --project /absolute/path/to/project
python3 scripts/inventory.py --project /absolute/path/to/project --project-id PROJECT_ID --alias /confirmed/old/project/path
python3 scripts/inventory.py --project /absolute/path/to/project --codex-home /path/to/codex-home
```

`--alias` 可重复传入，只应添加已确认属于所选项目的路径。默认使用 `CODEX_HOME`，未设置时使用 `~/.codex`。脚本匹配精确路径和可用的项目 ID，不自动包含子目录；扫描根目录及 `sqlite/` 下的 `state_*.sqlite`，按对话 ID 去重并保留来源。

输出 JSON 包含 `candidate_count`、`project_paths`、`databases`、`errors`、`coverage` 和 `threads`。退出码 0 表示发现的数据库均读取成功；1 表示存在读取错误或未发现数据库。候选数量不等于经应用核验的最终项目总数，数据库中的旧标题也不代表当前 UI 标题。

范围、时间、关键词和归档筛选由 skill 流程处理，脚本只负责候选清单，不执行改名。

## 隐私与限制

脚本以只读方式连接 SQLite，不联网、不修改数据库。清单可能包含标题、本地路径和对话 ID，分享问题报告前请脱敏。skill 阅读的对话内容仍受所使用 Codex 服务及账户设置约束，不代表整个流程离线运行。

应用列表可能不完整，数据库 schema 也可能变化。缺失历史、未知归属、远端不可访问等情况必须报告，不能用局部结果冒充全量处理。全文、摘要和仅标题模式会明确区分。

## 开发

```bash
python3 -m unittest discover -s tests -v
```

测试使用临时合成数据库，覆盖精确路径、别名、项目 ID、去重、只读与错误状态，不读取真实聊天。GitHub Actions 在 Python 3.9 和 3.13 上运行同一组测试。实际应用中的对话工具与改名行为需单独验证。

## 许可证

[MIT](LICENSE)。本项目是独立社区项目，不隶属于 OpenAI。
