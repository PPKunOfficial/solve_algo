import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "sync"


class SyncCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.remote = self.root / "remote.git"
        self.work = self.root / "work"

        self.run_git(self.root, "init", "-q", "--bare", "-b", "main", str(self.remote))
        self.run_git(self.root, "init", "-q", "-b", "main", str(self.work))
        self.work_git("config", "user.name", "Sync Test")
        self.work_git("config", "user.email", "sync@example.test")
        (self.work / "README").write_text("base\n", encoding="utf-8")
        self.work_git("add", "README")
        self.work_git("commit", "-q", "-m", "base")
        self.work_git("remote", "add", "origin", str(self.remote))
        self.work_git("push", "-q", "-u", "origin", "main")

    def run_git(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
        )

    def work_git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_git(self.work, *args)

    def sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *args],
            cwd=self.work,
            text=True,
            capture_output=True,
        )

    def work_head(self) -> str:
        return self.work_git("rev-parse", "HEAD").stdout.strip()

    def remote_head(self) -> str:
        return self.run_git(self.remote, "rev-parse", "main").stdout.strip()

    def test_commits_and_pushes_changes(self) -> None:
        (self.work / "solution.py").write_text("print(1)\n", encoding="utf-8")

        result = self.sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("同步完成", result.stdout)
        self.assertEqual(self.work_head(), self.remote_head())
        message = self.run_git(self.remote, "log", "-1", "--pretty=%s", "main").stdout.strip()
        self.assertTrue(message.startswith("同步更新 "), message)
        self.assertIn("（1 个文件）", message)

    def test_reports_already_synchronized(self) -> None:
        head_before = self.work_head()

        result = self.sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("已是最新", result.stdout)
        self.assertEqual(self.work_head(), head_before)
        self.assertEqual(self.remote_head(), head_before)

    def test_rebases_onto_remote_before_pushing(self) -> None:
        other = self.root / "other"
        self.run_git(self.root, "clone", "-q", str(self.remote), str(other))
        self.run_git(other, "config", "user.name", "Other")
        self.run_git(other, "config", "user.email", "other@example.test")
        (other / "remote-change.txt").write_text("remote\n", encoding="utf-8")
        self.run_git(other, "add", "remote-change.txt")
        self.run_git(other, "commit", "-q", "-m", "remote change")
        self.run_git(other, "push", "-q", "origin", "main")
        remote_head = self.run_git(other, "rev-parse", "HEAD").stdout.strip()

        (self.work / "local-change.txt").write_text("local\n", encoding="utf-8")
        result = self.sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.work_head(), self.remote_head())
        log = self.work_git("log", "--pretty=%s", "--max-count=3").stdout
        self.assertIn("remote change", log)
        self.assertIn("同步更新", log)
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", remote_head, "HEAD"], cwd=self.work
        )
        self.assertEqual(ancestor.returncode, 0)

    def test_dry_run_does_not_modify_repository(self) -> None:
        head_before = self.work_head()
        (self.work / "pending.py").write_text("pass\n", encoding="utf-8")

        result = self.sync("--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("pending.py", result.stdout)
        self.assertEqual(self.work_head(), head_before)
        self.assertEqual(self.remote_head(), head_before)
        self.assertIn("pending.py", self.work_git("status", "--porcelain").stdout)

    def test_refuses_to_commit_secrets(self) -> None:
        (self.work / ".env").write_text("TOKEN=secret\n", encoding="utf-8")
        head_before = self.work_head()

        result = self.sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("密钥", result.stderr)
        self.assertEqual(self.work_head(), head_before)

    def test_no_commit_pushes_existing_commits(self) -> None:
        (self.work / "committed.py").write_text("x = 1\n", encoding="utf-8")
        self.work_git("add", "committed.py")
        self.work_git("commit", "-q", "-m", "local only")
        local_head = self.work_head()

        result = self.sync("--no-commit")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.remote_head(), local_head)
        self.assertEqual(
            self.run_git(self.remote, "log", "-1", "--pretty=%s", "main").stdout.strip(),
            "local only",
        )


if __name__ == "__main__":
    unittest.main()
