import sys
from pathlib import Path
import unittest.mock as mock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
from gui import MetadataAnalyzerApp


@pytest.fixture
def app():
    """Create application instance for testing."""
    return MetadataAnalyzerApp()


def test_metadata_analyzer_app_init():
    """Test application initialization."""
    app = MetadataAnalyzerApp()
    assert app is not None
    assert app.file_path is None
    assert app.extracted_metadata == {}


def test_app_has_required_attributes():
    """Test that app has all required attributes."""
    app = MetadataAnalyzerApp()
    
    # Check core state attributes
    assert hasattr(app, 'file_path')
    assert hasattr(app, 'extracted_metadata')
    assert hasattr(app, 'root')
    assert hasattr(app, 'c1_text')
    assert hasattr(app, 'status_var')
    assert hasattr(app, 'progress_var')


def test_app_has_required_methods():
    """Test that app has all required methods."""
    app = MetadataAnalyzerApp()
    
    # Check core methods
    assert hasattr(app, 'run')
    assert callable(app.run)
    assert hasattr(app, 'set_status')
    assert callable(app.set_status)
    assert hasattr(app, '_is_editable_field')
    assert callable(app._is_editable_field)


def test_app_non_editable_fields():
    """Test that NON_EDITABLE_FIELDS is properly defined."""
    assert hasattr(MetadataAnalyzerApp, 'NON_EDITABLE_FIELDS')
    non_editable = MetadataAnalyzerApp.NON_EDITABLE_FIELDS
    
    assert "File Name" in non_editable
    assert "File Size" in non_editable
    assert "File Type" in non_editable
    assert "Extracted At" in non_editable
    assert "Modified On" in non_editable


def test_is_editable_field_editable(app):
    """Test _is_editable_field with editable field."""
    result = app._is_editable_field("Title")
    assert result is True


def test_is_editable_field_non_editable(app):
    """Test _is_editable_field with non-editable field."""
    result = app._is_editable_field("File Name")
    assert result is False


def test_set_status(app):
    """Test set_status method."""
    # Mock the status_var
    with mock.patch.object(app, 'status_var') as mock_var:
        app.set_status("Test message")
        mock_var.set.assert_called_once_with("Test message")


def test_clear_editor_fields(app):
    """Test _clear_editor_fields method."""
    # Mock the editor entry frame
    with mock.patch.object(app, 'editor_entry_frame') as mock_frame:
        mock_frame.winfo_children.return_value = []
        app._clear_editor_fields()
        assert app.editor_entry_fields == {}


def test_app_initialization_values(app):
    """Test that app initializes with correct default values."""
    assert app.file_path is None
    assert app.extracted_metadata == {}
    assert app.root is None
    assert app.c1_text is None
    assert app.progress_var is None
    assert app.progress_bar is None
    assert app.nb_widget is None
    assert app.tab2_ref is None
    assert app.tab4_ref is None
    assert app.editor_entry_fields == {}
    assert app.editor_entry_frame is None
    assert app.editor_canvas is None
    assert app.editor_status is None
    assert app.report_preview is None
    assert app.report_image_label is None
    assert app.window_width is None
    assert app.window_height is None
    assert app.x_position is None
    assert app.y_position is None
    assert app.report_last_text == ""
    assert app.history_refresh is None
    assert app.stats_cache is None
    assert app.stats_cache_time is None
    assert app.stats_cache_duration == 30


def test_app_zoom_attributes(app):
    """Test that app has zoom-related attributes."""
    assert hasattr(app, 'preview_image_zoom')
    assert app.preview_image_zoom == 1.0
    assert hasattr(app, 'preview_base_image')
    assert app.preview_base_image is None
    assert hasattr(app, 'preview_canvas')
    assert app.preview_canvas is None
    assert hasattr(app, 'preview_scrollbar')
    assert app.preview_scrollbar is None


# Backward compatibility wrapper
def test_metadata_Analyzer_app_init():
    """Backward compatibility wrapper. See test_metadata_analyzer_app_init for details."""
    test_metadata_analyzer_app_init()
