import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
from gui import MetadataAnalyzerApp

def test_metadata_Analyzer_app_init():
    app = MetadataAnalyzerApp()
    assert app is not None
