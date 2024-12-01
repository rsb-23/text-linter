import os
import subprocess

import requests

from groq_ai import find_typos


def process_diff(file_path, base_branch):
    try:
        # Get diff from PR
        diff_command = f"git diff -U0 origin/{base_branch}... -- {file_path}"
        diff_output = subprocess.check_output(diff_command.split()).decode("utf-8")
    except subprocess.CalledProcessError:
        print("Error in process diff")
        return -1

    # only checks for typos in added text
    new_text = "".join(x for x in diff_output.splitlines(keepends=True) if x.startswith("+"))
    return find_typos(new_text) if new_text else -1


def post_comment(comment):
    pr_no = os.environ["PR_NO"]
    repo = os.environ["repo"]
    url = f"https://api.github.com/repos/{repo}/issues/{pr_no}/comments"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['token']}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.post(url, headers=headers, json={"body": comment})
    resp.raise_for_status()


def main():
    # Get required inputs
    pr_base = os.environ["PR_BASE"]
    files = [*map(str.strip, os.environ["INPUT_FILES"].splitlines())]
    print(pr_base, *files, sep="\n")

    results = {file_path: process_diff(file_path, pr_base) for file_path in files if file_path}

    # Create markdown comment for fixes
    flag = False
    comment = "### Suggested Typo Fixes\n"
    for file_path, suggestion in results.items():
        if suggestion == -1:
            continue
        suggestion = "\n  ".join(suggestion)
        comment += f"- {file_path}:\n  {suggestion}\n"
        flag = True
    if flag:
        comment += "\n**Tip**: Create a commit in this PR itself."
    else:
        comment = "### No typos found"

    print(comment)
    post_comment(comment)


if __name__ == "__main__":
    main()
