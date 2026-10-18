# Codex Project Chat Renamer

Inventory and rename Codex chats in **any project you choose**: the current project, another project, or several projects.

[中文](README.md) · [Skill instructions](SKILL.md) · [Contributing](CONTRIBUTING.md) · [MIT](LICENSE)

## Features

Choose projects, archived status, user or subagent chats, date and keyword filters, and explicit chat IDs. Choose inventory only, preview, or direct execution. Read full history, use summaries, or normalize existing titles. Customize prefixes, language, length, templates, duplicate handling, and JSON/CSV export.

The target project is a user choice. The working directory alone does not select a target. Preview and inventory requests never authorize title changes.

## Requirements and installation

This is a skill instruction package, not a standalone renaming app. The full workflow requires a Codex environment exposing project/chat tools such as `list_projects`, `list_threads`, `read_thread`, `list_archived_threads`, and `set_thread_title`. Installing this repository does not provide those tools. Without them, only supported inventory or proposed mappings can be delivered.

The local inventory helper requires Python 3.9+ and uses only the standard library.

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/Snake-Konginchrist/codex-project-chat-renamer.git ~/.agents/skills/codex-project-chat-renamer
```

Do not overwrite an existing installation. Restart Codex if the skill does not appear. See the [official skill documentation](https://developers.openai.com/codex/skills) for local discovery. This repository distributes standalone source, not a plugin-directory listing.

## Examples

```text
Use $codex-project-chat-renamer. Let me choose one or more projects and naming rules, then show a preview.
```

```text
Use $codex-project-chat-renamer for Atlas and Beacon. Read full history,
use a separate project prefix for each, and preview the proposed titles in English.
```

```text
Use $codex-project-chat-renamer to count archived chats in Beacon. Do not rename them.
```

Defaults: user-selected projects, unarchived user chats, full-history reading, concise Chinese topics with no added prefix and a 16-character topic limit. Ask for English or another language as needed. Existing compliant titles are skipped unless the user requests rewriting. See [SKILL.md](SKILL.md) for the complete Chinese workflow.

## Inventory helper

Run from the repository:

```bash
python3 scripts/inventory.py --project /absolute/project/path --project-id PROJECT_ID
python3 scripts/inventory.py --project /absolute/project/path --alias /confirmed/old/path --codex-home /path/to/codex-home
```

`--project-id`, repeatable `--alias`, and `--codex-home` are optional. The default home is `CODEX_HOME` or `~/.codex`. The helper reads `state_*.sqlite` in that directory and its `sqlite/` subdirectory, matches exact paths or project IDs, and deduplicates IDs while retaining sources. It does not recursively include child projects or rename chats. Other filters are applied by the skill workflow.

JSON contains candidate counts, paths, inspected databases, errors, coverage notes, and thread records. Exit 0 means all discovered databases were inspected; exit 1 means an error occurred or no databases were found. Candidates and stored titles must be reconciled with the application. Local data does not establish remote-host completeness.

## Privacy and validation

The helper opens SQLite read-only and makes no network requests. Output can contain private titles, paths, and chat IDs: redact it before sharing. The skill runs within your Codex service and account settings; the whole workflow is not necessarily offline.

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic temporary databases, never real chats. CI runs on Python 3.9 and 3.13. These tests do not validate live application title changes.

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE). Independent community project, not affiliated with OpenAI.
