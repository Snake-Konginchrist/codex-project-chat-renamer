import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory.py"


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name).resolve()
        self.project = str(self.home / "project")

    def database(self, name, rows, extended=False):
        path = self.home / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE threads (id TEXT, cwd TEXT" + (", project_id TEXT" if extended else "") + ")")
            db.executemany("INSERT INTO threads VALUES (" + ",".join("?" for _ in range(3 if extended else 2)) + ")", rows)
        return path

    def run_inventory(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), "--project", self.project,
                                 "--codex-home", str(self.home), *args], capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def test_exact_path_excludes_children_and_preserves_database(self):
        path = self.database("state_1.sqlite", [("match", self.project), ("child", self.project + "/child")])
        before = path.read_bytes()
        code, data = self.run_inventory()
        self.assertEqual(code, 0)
        self.assertEqual([t["id"] for t in data["threads"]], ["match"])
        self.assertEqual(path.read_bytes(), before)

    def test_alias_project_id_and_duplicate_sources(self):
        alias = str(self.home / "old")
        self.database("state_1.sqlite", [("same", self.project), ("alias", alias)])
        self.database("sqlite/state_2.sqlite", [("same", self.project, "p"), ("member", "/elsewhere", "p"), ("other", "/elsewhere", "q")], True)
        code, data = self.run_inventory("--alias", alias, "--project-id", "p")
        self.assertEqual(code, 0)
        self.assertEqual(data["candidate_count"], 3)
        records = {t["id"]: t["records"] for t in data["threads"]}
        self.assertEqual(set(records), {"same", "alias", "member"})
        self.assertEqual(len(records["same"]), 2)

    def test_partial_error_preserves_valid_candidates(self):
        self.database("state_1.sqlite", [("ok", self.project)])
        (self.home / "state_bad.sqlite").write_text("invalid database")
        code, data = self.run_inventory()
        self.assertEqual(code, 1)
        self.assertEqual(data["candidate_count"], 1)
        self.assertEqual(len(data["errors"]), 1)

    def test_missing_database_and_unsupported_schema(self):
        code, data = self.run_inventory()
        self.assertEqual(code, 1)
        self.assertEqual(data["databases"], [])
        with sqlite3.connect(self.home / "state_empty.sqlite") as db:
            db.execute("CREATE TABLE unrelated (id TEXT)")
        code, data = self.run_inventory()
        self.assertEqual(code, 1)
        self.assertIn("schema lacks", data["errors"][0]["error"])

    def test_valid_empty_inventory(self):
        self.database("state_1.sqlite", [])
        code, data = self.run_inventory()
        self.assertEqual(code, 0)
        self.assertEqual(data["candidate_count"], 0)
        self.assertEqual(data["errors"], [])


if __name__ == "__main__":
    unittest.main()
