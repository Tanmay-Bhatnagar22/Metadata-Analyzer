import sys
from pathlib import Path
import unittest.mock as mock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
from main import main


def test_main_callable():
    """Test that main function is callable."""
    assert callable(main)


def test_main_function_exists():
    """Test that main function is defined."""
    import main as main_module
    assert hasattr(main_module, 'main')


def test_main_handles_gui_launch():
    """Test that main function attempts to launch GUI."""
    # Mock the run_gui function to prevent actual GUI launch
    with mock.patch('main.run_gui') as mock_run_gui:
        main()
        mock_run_gui.assert_called_once()


def test_main_handles_exceptions():
    """Test that main function handles GUI launch exceptions."""
    # Mock run_gui to raise an exception
    with mock.patch('main.run_gui', side_effect=Exception("GUI Error")):
        # Should not raise, just print error
        try:
            main()
        except Exception:
            pytest.fail("main() should handle exceptions gracefully")
