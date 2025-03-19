import subprocess

import requests

from src.config import ENVIRONMENT, GitEnv
from src.llm_service import find_typos, validate_model


def process_diff(file_path, base_branch=GitEnv.PR_BASE):
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
    print(comment)
    if ENVIRONMENT == "local":
        return

    url = f"https://api.github.com/repos/{GitEnv.REPO}/issues/{GitEnv.PR_NO}/comments"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GitEnv.PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.post(url, headers=headers, json={"body": comment}, timeout=300)
    resp.raise_for_status()


def main():
    validate_model()
    # Process diff(s) for each file
    results = {file_path: process_diff(file_path) for file_path in GitEnv.INPUT_FILES if file_path}

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

    post_comment(comment)


if __name__ == "__main__":
    main()
