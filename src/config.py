import os


def get_env(x):
    return os.environ[x]


GROQ_API_KEY = get_env("GROQ_API_KEY")
PAT_TOKEN = get_env("token")

REPO = get_env("GITHUB_REPOSITORY")
PR_BASE = get_env("PR_BASE")
PR_NO = get_env("PR_NO")
INPUT_FILES = [*map(str.strip, get_env("INPUT_FILES").splitlines())]
