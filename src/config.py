import os
from dataclasses import dataclass


def get_env(x, optional=False):
    return os.environ.get(x) if optional else os.environ[x]


ENVIRONMENT = get_env("ENVIRONMENT", optional=True)


@dataclass
class GitEnv:
    PAT_TOKEN = get_env("token")
    REPO = get_env("GITHUB_REPOSITORY")
    PR_BASE = get_env("PR_BASE")
    PR_NO = get_env("PR_NO")
    INPUT_FILES = [*map(str.strip, get_env("INPUT_FILES").splitlines())]


PROVIDER = get_env("PROVIDER").lower()
LLM_API_KEY = get_env("API_KEY")
LLM_MODELS = {"openai": "gpt-3.5-turbo", "anthropic": "claude-3-haiku-20240307", "groq": "llama3-70b-8192"}
LLM_MODEL = get_env("LLM_MODEL", optional=True) or LLM_MODELS[PROVIDER]
