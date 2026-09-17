import sys
import argparse
from .git import get_git_commits
from .formatter import format_commits_to_tree, format_commits_to_contributions
from rich.console import Console


def main():
    console = Console(highlight=False)

    parser = argparse.ArgumentParser(description="Visual Git log timeline.")
    parser.add_argument("-n", "--limit", type=int, default=10,
                        help="Number of commits to display.")
    parser.add_argument("--author", type=str, help="Filter commits by author.")
    parser.add_argument("--no-colour", "--no-color",
                        action="store_true", help="Disable coloured options.")

    args = parser.parse_args()

    try:
        commits = get_git_commits(author=args.author, limit=args.limit)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not commits:
        print("No commits match the given arguments.")
        sys.exit(0)

    use_colour = not args.no_colour
    log_timeline = format_commits_to_tree(commits, use_colour)
    log_contributions = format_commits_to_contributions(commits)

    for commit in log_timeline:
        console.print(commit)

    for contributor in log_contributions:
        console.print(contributor)


if __name__ == '__main__':
    main()
