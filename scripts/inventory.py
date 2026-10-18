#!/usr/bin/env python3
"""Read-only local Codex thread inventory; titles are candidates, not UI truth."""
import argparse
import json
import os
import sqlite3
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--project-id')
    parser.add_argument('--alias', action='append', default=[])
    parser.add_argument('--codex-home', default=os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    args = parser.parse_args()
    home = Path(args.codex_home).expanduser().resolve()
    paths = sorted({str(Path(p).expanduser().resolve()) for p in [args.project, *args.alias]})
    databases = sorted(set(home.glob('state_*.sqlite')) | set((home / 'sqlite').glob('state_*.sqlite')))
    found, inspected, errors = {}, [], []
    for database in databases:
        try:
            connection = sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True)
            try:
                connection.execute('PRAGMA query_only=ON')
                columns = {r[1] for r in connection.execute('PRAGMA table_info(threads)')}
                if not {'id', 'cwd'} <= columns:
                    raise ValueError('threads schema lacks id/cwd')
                wanted = [c for c in ['id', 'cwd', 'title', 'project_id', 'archived', 'source', 'agent_role', 'rollout_path'] if c in columns]
                where = 'cwd IN (' + ','.join('?' for _ in paths) + ')'
                params = list(paths)
                if args.project_id and 'project_id' in columns:
                    where += ' OR project_id = ?'
                    params.append(args.project_id)
                query = 'SELECT ' + ','.join(wanted) + ' FROM threads WHERE ' + where
                rows = connection.execute(query, params).fetchall()
                for row in rows:
                    record = dict(zip(wanted, row))
                    found.setdefault(record['id'], []).append({'database': str(database), **record})
                inspected.append({'database': str(database), 'matches': len(rows)})
            finally:
                connection.close()
        except (sqlite3.Error, ValueError, OSError) as error:
            errors.append({'database': str(database), 'error': str(error)})
    print(json.dumps({'candidate_count': len(found), 'project_paths': paths,
                      'databases': inspected, 'errors': errors,
                      'coverage': 'Local database candidates only; reconcile application membership, archives, titles and hosts.',
                      'threads': [{'id': key, 'records': value} for key, value in sorted(found.items())]}, ensure_ascii=False, indent=2))
    return 1 if errors or not databases else 0


if __name__ == '__main__':
    raise SystemExit(main())
