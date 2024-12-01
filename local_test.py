from src.spell_check import main


def run():
    from dotenv import load_dotenv

    load_dotenv()
    main()


if __name__ == "__main__":
    run()
