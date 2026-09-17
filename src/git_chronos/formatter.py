from .git import Commit
from .git import get_git_commits
from collections import defaultdict
from rich.console import Console

DATE_STRING_LENGTH = 12
CONTRIBUTION_BAR_LENGTH = 18


def group_commits_by(commits: list[Commit], group_by: str) -> dict[list[Commit]]:
    if not group_by in Commit.__annotations__:
        raise AttributeError(f"Cannot group commits by '{group_by}'")

    grouped_commits = defaultdict(list)

    for commit in commits:
        grouped_commits[getattr(commit, group_by)].append(commit)

    return grouped_commits


def colourize_commit_fields(commit: Commit) -> Commit:
    colour_hash = f"[gray]{commit.hash}[/gray]"
    colour_author = f"[bold cyan]{commit.author}[/bold cyan]"
    colour_date = f"{commit.date}"
    colour_message = f"[bold white]{commit.message}[/bold white]"
    colourized_commit = Commit(colour_hash,
                               colour_author,
                               colour_date,
                               colour_message)

    return colourized_commit


def format_commits_to_tree(commits: list[Commit], colourized: bool = True) -> list[str]:
    output = []

    commits_grouped_by_date = group_commits_by(commits, "date")

    number_of_days = len(commits_grouped_by_date)
    vertical_separator = " " * DATE_STRING_LENGTH + "\x09┃"

    for i, date in enumerate(commits_grouped_by_date.keys()):
        number_of_commits = len(commits_grouped_by_date[date])
        is_first_in_date = True
        for j, commit in enumerate(commits_grouped_by_date[date]):
            is_first_commit = i >= number_of_days - 1 and j >= number_of_commits - 1

            colourized_commit = commit
            if colourized:
                colourized_commit = colourize_commit_fields(commit)

            if is_first_in_date:
                formatted_commit = f"[{colourized_commit.date}]\x09"
                is_first_in_date = False
            else:
                formatted_commit = " " * DATE_STRING_LENGTH + "\x09"

            formatted_commit += "━━━━━" * (not is_first_commit) + "●\x09" +\
                f"({colourized_commit.author})\x09" +\
                f"{colourized_commit.message}"

            output.append(formatted_commit)

            if not is_first_commit:
                output.append(vertical_separator)

    return output


def format_commits_to_contributions(commits: list[Commit]) -> list[str]:
    output = ["Contributions:"]

    commits_grouped_by_author = group_commits_by(commits, "author")

    contribution_counts = defaultdict(int)
    total_commits = 0

    for author, commits in commits_grouped_by_author.items():
        contribution_counts[author] = len(commits)
        total_commits += len(commits)

    for author, count in contribution_counts.items():
        frequency = count / total_commits
        bar_full_count = (int)(frequency * CONTRIBUTION_BAR_LENGTH)

        contriubtion_bar = "█" * bar_full_count + "░" * \
            (CONTRIBUTION_BAR_LENGTH - bar_full_count)
        output.append(
            f"{author}\x09[{contriubtion_bar}] {(int) (frequency * 100)}% ({count} commits)")

    return output


if __name__ == '__main__':
    commits = get_git_commits()
    pretty_commits = format_commits_to_tree(commits, False)
    contriubtion_list = format_commits_to_contributions(commits)

    console = Console()

    for commit in pretty_commits:
        console.print(commit)

    for commit in contriubtion_list:
        console.print(commit)
