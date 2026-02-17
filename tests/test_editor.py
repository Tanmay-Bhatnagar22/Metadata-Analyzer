import sys
from pathlib import Path
import tempfile
import os
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
from editor import (
    MetadataEditor, parse_editor_text, validate_metadata, 
    get_editable_text, clear_editor, write_metadata_to_file,
    can_write_metadata
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def sample_metadata():
    """Sample metadata for testing."""
    return {
        "Title": "Test Document",
        "Author": "Test Author",
        "Subject": "Test Subject"
    }


def test_metadata_editor_init():
    """Test editor initialization."""
    editor = MetadataEditor()
    assert editor is not None
    assert editor.db_client is not None


def test_parse_editor_text_basic():
    """Test parsing basic editor text."""
    text = "File Name: test.txt\nFile Size: 1.0 KB\nAuthor: Test"
    result = parse_editor_text(text)
    
    assert isinstance(result, dict)
    assert "headers" in result
    assert "metadata" in result


def test_parse_editor_text_with_headers():
    """Test parsing editor text with standard headers."""
    text = "File Name: test.txt\nFile Size: 1.0 KB\nFile Type: txt\nTitle: Test Document"
    result = parse_editor_text(text)
    
    headers = result["headers"]
    assert headers.get("File Name") == "test.txt"
    assert headers.get("File Size") == "1.0 KB"
    assert headers.get("File Type") == "txt"


def test_parse_editor_text_with_custom_metadata():
    """Test parsing editor text with custom metadata."""
    text = "File Name: doc.pdf\nCustom Field: Custom Value\nAnother: Value"
    result = parse_editor_text(text)
    
    metadata = result["metadata"]
    assert metadata.get("Custom Field") == "Custom Value"
    assert metadata.get("Another") == "Value"


def test_parse_editor_text_empty():
    """Test parsing empty text."""
    result = parse_editor_text("")
    
    assert result["headers"] == {}
    assert result["metadata"] == {}


def test_parse_editor_text_no_colons():
    """Test parsing text with no colons."""
    text = "Invalid line\nAnother invalid"
    result = parse_editor_text(text)
    
    assert result["headers"] == {}
    assert result["metadata"] == {}


def test_validate_metadata_valid():
    """Test validation with valid metadata."""
    parsed = {
        "headers": {"File Name": "test.txt"},
        "metadata": {"Title": "Test"}
    }
    valid, msg = validate_metadata(parsed)
    
    assert valid is True
    assert msg == ""


def test_validate_metadata_missing_filename():
    """Test validation with missing File Name."""
    parsed = {
        "headers": {},
        "metadata": {"Title": "Test"}
    }
    valid, msg = validate_metadata(parsed)
    
    assert valid is False
    assert "File Name" in msg


def test_validate_metadata_empty_metadata():
    """Test validation with empty metadata."""
    parsed = {
        "headers": {"File Name": "test.txt"},
        "metadata": {}
    }
    valid, msg = validate_metadata(parsed)
    
    assert valid is False
    assert "cannot be empty" in msg


def test_get_editable_text(temp_dir, sample_metadata):
    """Test building editable text from metadata."""
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("content")
    
    editor = MetadataEditor()
    text = editor.get_editable_text(test_file, sample_metadata)
    
    assert isinstance(text, str)
    assert "File Name" in text
    assert "test.txt" in text


def test_get_editable_text_with_empty_metadata(temp_dir):
    """Test building editable text with empty metadata."""
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("content")
    
    editor = MetadataEditor()
    text = editor.get_editable_text(test_file, {})
    
    assert isinstance(text, str)
    assert "File Name" in text


def test_get_editable_text_with_nonexistent_file():
    """Test building editable text with non-existent file."""
    editor = MetadataEditor()
    text = editor.get_editable_text("/nonexistent/file.txt", {"Title": "Test"})
    
    assert isinstance(text, str)
    assert "File Name" in text


def test_clear_editor():
    """Test clear_editor function."""
    text = clear_editor()
    
    assert isinstance(text, str)
    assert "No metadata loaded" in text


def test_can_write_metadata(temp_dir):
    """Test can_write_metadata function."""
    test_file = os.path.join(temp_dir, "test.txt")
    
    # Should always return True in current implementation
    result = can_write_metadata(test_file)
    assert result is True


def test_write_metadata_to_file_unsupported_format(temp_dir, sample_metadata):
    """Test writing metadata to unsupported file format."""
    test_file = os.path.join(temp_dir, "test.xyz")
    with open(test_file, "w") as f:
        f.write("content")
    
    editor = MetadataEditor()
    success, msg = editor.write_metadata_to_file(test_file, sample_metadata)
    
    # Should handle unsupported formats gracefully
    assert isinstance(success, bool)


def test_write_metadata_to_file_nonexistent():
    """Test writing metadata to non-existent file."""
    editor = MetadataEditor()
    success, msg = editor.write_metadata_to_file("/nonexistent/file.txt", {"Title": "Test"})
    
    assert success is False
    assert "File not found" in msg


def test_write_text_metadata(temp_dir, sample_metadata):
    """Test writing metadata to text file."""
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("Original content")
    
    editor = MetadataEditor()
    success, msg = editor.write_text_metadata(test_file, sample_metadata)
    
    assert success is True
    assert "metadata written" in msg.lower()
    
    # Verify backup was cleaned up
    assert not os.path.exists(test_file + ".backup")


def test_write_generic_metadata(temp_dir, sample_metadata):
    """Test writing generic metadata (companion file)."""
    test_file = os.path.join(temp_dir, "test.unknown")
    with open(test_file, "w") as f:
        f.write("content")
    
    editor = MetadataEditor()
    success, msg = editor.write_generic_metadata(test_file, sample_metadata)
    
    assert success is True
    assert "companion file" in msg.lower()
    
    # Verify companion file was created
    companion = test_file + ".meta.json"
    assert os.path.exists(companion)
    
    # Verify companion file content
    with open(companion, "r") as f:
        data = json.load(f)
    assert data["metadata"] == sample_metadata


def test_wrapper_functions():
    """Test module-level wrapper functions."""
    # Test parse_editor_text
    result = parse_editor_text("File Name: test.txt")
    assert isinstance(result, dict)
    
    # Test validate_metadata
    valid, msg = validate_metadata({"headers": {}, "metadata": {}})
    assert isinstance(valid, bool)
    
    # Test get_editable_text
    text = get_editable_text("test.txt", {})
    assert isinstance(text, str)
    
    # Test clear_editor
    text = clear_editor()
    assert isinstance(text, str)


# Backward compatibility wrappers
def test_parse_editor_text():
    """Backward compatibility wrapper. See test_parse_editor_text_basic for details."""
    test_parse_editor_text_basic()


def test_validate_metadata():
    """Backward compatibility wrapper. See test_validate_metadata_valid for details."""
    test_validate_metadata_valid()


def test_save_edited_metadata():
    """Backward compatibility wrapper. See test_write_text_metadata for details."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("content")
        editor = MetadataEditor()
        success, msg = editor.write_text_metadata(test_file, {"Title": "Test"})
        assert success is True


def test_write_metadata_to_file():
    """Backward compatibility wrapper. See test_write_metadata_to_file_unsupported_format for details."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.xyz")
        with open(test_file, "w") as f:
            f.write("content")
        editor = MetadataEditor()
        success, msg = editor.write_metadata_to_file(test_file, {"Title": "Test"})
        assert isinstance(success, bool)
