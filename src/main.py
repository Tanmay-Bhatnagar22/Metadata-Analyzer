"""Main entry point for Metadata Analyzer application."""

from gui import run_gui


def main() -> None:
    """Launch the Metadata Analyzer GUI application.
    
    Entry point for the application. Initializes and runs the Tkinter-based GUI.
    """
    try:
        run_gui()
    except Exception as exc:
        # Avoid crashing silently; surface the startup issue to the console.
        print(f"Failed to launch GUI: {exc}")


if __name__ == "__main__":
    main()
