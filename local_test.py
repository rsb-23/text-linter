from dotenv import load_dotenv, set_key

load_dotenv()

set_key(".env", "ENVIRONMENT", "local")

if __name__ == "__main__":
    from src.text_linter import main

    main()
