import os


def get_env(x, default=None):
    return os.environ.get(x, default)


PROVIDER = get_env("PROVIDER", default="groq").upper()
LLM_API_KEY = get_env("API_KEY")
os.environ[f"{PROVIDER}_API_KEY"] = LLM_API_KEY

PAT_TOKEN = get_env("token")

REPO = get_env("GITHUB_REPOSITORY")
PR_BASE = get_env("PR_BASE")
PR_NO = get_env("PR_NO")
INPUT_FILES = [*map(str.strip, get_env("INPUT_FILES").splitlines())]

LLM_MODELS = {"OPENAI": "gpt-3.5-turbo", "ANTHROPIC": "claude-3-haiku-20240307", "GROQ": "llama3-70b-8192"}
LLM_MODEL = get_env("LLM_MODEL") or LLM_MODELS[PROVIDER]
