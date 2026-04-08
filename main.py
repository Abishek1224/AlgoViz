def main() -> None:
    try:
        import pygame  # noqa: F401
        from algoviz.app import AlgoVizApp
    except ModuleNotFoundError:
        print("AlgoViz could not start because pygame is not installed.")
        print("Quick fix:")
        print("  1) pip install -r requirements.txt")
        print("  2) python main.py")
        print("If installation fails, use Python 3.12/3.13 in a virtual environment.")
        return

    app = AlgoVizApp()
    app.run()


if __name__ == "__main__":
    main()
