# Contributing

[简体中文](CONTRIBUTING.zh-CN.md)

Contributions to naming options, project selection, history coverage checks, and database compatibility are welcome.

## Development

1. Fork and clone the repository, then create a working branch.
2. Keep `SKILL.md`, `agents/openai.yaml`, and both READMEs consistent when changing skill behavior.
3. Add meaningful tests for script changes using synthetic temporary databases.
4. Run `python3 -m unittest discover -s tests -v`.
5. Open a pull request describing the problem, changes, and validation scope.

Keep English documentation in unsuffixed files and Simplified Chinese translations in `.zh-CN.md` files.

Preserve user-selected projects, preview-only behavior, read-only database access, and application-based title writes. Summary-based reading must not be presented as full-history reading. Never claim successful renaming without the necessary application tools and verification.

## Reporting issues

Include expected behavior, actual results, your Python version, and a minimal redacted reproduction. For database compatibility issues, prefer field names and synthetic examples.

Do not upload real chat histories, databases, access tokens, or private paths in issues or test fixtures.
