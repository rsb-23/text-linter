import os
import tempfile

from src.spell_check import main


def run():
    if "GITHUB_OUTPUT" not in os.environ:
        from dotenv import load_dotenv

        load_dotenv()
        with tempfile.NamedTemporaryFile(mode="w+", delete_on_close=False) as f:
            os.environ["GITHUB_OUTPUT"] = f.name
            main()


if __name__ == "__main__":
    run()
