import sys
import subprocess
from dataclasses import dataclass


@dataclass
class Commit:
    hash: str
    author: str
    date: str
    message: str


def process_commit_string(commit: str) -> Commit:
    hash, author, date, message = commit.split("\x09")

    return Commit(hash, author, date, message)


def get_git_commits(author: str | None = None, limit: int = 10) -> list[Commit]:
    cmd_args = ["git", "log", f"-n{limit}",
                '--pretty=format:%h\x09%an\x09%ad\x09%s', "--date=short"]

    if author:
        cmd_args.append(f"author={author}")

    try:
        commit_log = subprocess.run(
            cmd_args, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: The current directory is not a Git repository.", file=sys.stderr)
        sys.exit(1)

    commit_strings = commit_log.stdout.split("\n")

    commits = []

    for commit in commit_strings:
        commits.append(process_commit_string(commit))

    return commits


if __name__ == '__main__':
    print(get_git_commits())
