import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "lc-commit"


class LeetCodeCommitCliTest(unittest.TestCase):
    def test_commits_only_solution_with_header_message(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)

            def git(*args: str) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    ["git", *args],
                    cwd=repository,
                    check=True,
                    text=True,
                    capture_output=True,
                )

            git("init", "-q")
            git("config", "user.name", "CLI Test")
            git("config", "user.email", "cli@example.test")
            (repository / "README").write_text("base\n", encoding="utf-8")
            git("add", "README")
            git("commit", "-q", "-m", "base")

            (repository / "p0004.rs").write_text(
                "/*\n"
                " * @lc app=leetcode.cn id=4 lang=rust\n"
                " *\n"
                " * [4] 寻找两个正序数组的中位数\n"
                " */\n",
                encoding="utf-8",
            )
            (repository / "unrelated.txt").write_text("staged\n", encoding="utf-8")
            git("add", "unrelated.txt")

            subprocess.run(
                [str(SCRIPT), "p0004.rs"],
                cwd=repository,
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertEqual(
                git("log", "-1", "--pretty=%s").stdout.strip(),
                "[4] 寻找两个正序数组的中位数 rust",
            )
            self.assertEqual(
                git("show", "--pretty=", "--name-only", "HEAD").stdout.split(),
                ["p0004.rs"],
            )
            self.assertEqual(
                git("diff", "--cached", "--name-only").stdout.split(),
                ["unrelated.txt"],
            )


if __name__ == "__main__":
    unittest.main()
