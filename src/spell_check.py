import json
import os
import subprocess

from .groq_ai import find_typos


def process_diff(file_path):
    try:
        # Get diff from PR
        diff_command = f"git diff -U0 -- {file_path}"
        diff_output = subprocess.check_output(diff_command.split()).decode("utf-8")
    except subprocess.CalledProcessError:
        print("Error in process diff")
        return 0

    # only checks for typos in added text
    new_text = "".join(x for x in diff_output.splitlines(keepends=True) if x.startswith("+"))
    return find_typos(new_text) if new_text else -1


def main():
    # Get required inputs
    files = [*map(str.strip, os.environ["INPUT_FILES"].splitlines())]
    print(*files)

    results = {file_path: process_diff(file_path) for file_path in files if file_path}

    # Create markdown comment for fixes
    flag = False
    comment = "## Suggested Typo Fixes\n\n"
    for file_path, suggestion in results.items():
        if suggestion == -1:
            continue
        suggestion = "\n  ".join(suggestion)
        comment += f"- {file_path}:\n  {suggestion}\n"
        flag = True
    if flag:
        comment += "\n**Tip**: Create a commit in this PR itself."
    else:
        comment = ""

    # Set output for GitHub Actions
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"comment={json.dumps(comment)}\n")
    print(comment)


if __name__ == "__main__":
    main()
