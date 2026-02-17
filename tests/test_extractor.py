import sys
from pathlib import Path
import tempfile
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pytest
from extractor import (
    MetadataExtractor, extract_pdf_metadata, extract_text_metadata,
    extract, extract_and_store, batch_extract
)
from PyPDF2 import PdfWriter


class DummyDB:
    """In-memory stub used to capture insert calls."""

    def __init__(self):
        self.saved = []

    def insert_metadata(self, file_path, metadata):
        entry = {"file_path": str(file_path), "metadata": metadata}
        self.saved.append(entry)
        return (len(self.saved), file_path, os.path.basename(file_path), "1.0 KB", "txt", "2024-01-01", "2024-01-01", "")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_metadata_extractor_init():
    """Test extractor initialization."""
    extractor_obj = MetadataExtractor()
    assert extractor_obj is not None
    assert extractor_obj.db_client is not None


def test_extractor_with_custom_db():
    """Test extractor with custom database client."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    assert extractor_obj.db_client == db_client


def test_validate_file_path_valid(temp_dir):
    """Test file path validation with valid file."""
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("test content")
    
    is_valid, error = MetadataExtractor._validate_file_path(test_file)
    assert is_valid is True
    assert error == ""


def test_validate_file_path_missing_file():
    """Test file path validation with missing file."""
    is_valid, error = MetadataExtractor._validate_file_path("/nonexistent/path/file.txt")
    assert is_valid is False
    assert "File not found" in error


def test_validate_file_path_empty():
    """Test file path validation with empty path."""
    is_valid, error = MetadataExtractor._validate_file_path("")
    assert is_valid is False
    assert "No file path provided" in error


def test_validate_file_path_directory(temp_dir):
    """Test file path validation with directory instead of file."""
    is_valid, error = MetadataExtractor._validate_file_path(temp_dir)
    assert is_valid is False
    assert "not a file" in error


def test_extract_text_metadata(temp_dir):
    """Test text metadata extraction."""
    test_file = os.path.join(temp_dir, "sample.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("first line\nsecond line\n")
    
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract_text_metadata(test_file)
    
    assert meta["Line Count"] == 2
    assert meta["Encoding"] == "utf-8"
    assert meta["File Size (bytes)"] > 0


def test_extract_text_metadata_empty_file(temp_dir):
    """Test text metadata extraction from empty file."""
    test_file = os.path.join(temp_dir, "empty.txt")
    with open(test_file, "w") as f:
        pass
    
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract_text_metadata(test_file)
    
    assert meta["Line Count"] == 0


def test_extract_pdf_metadata(temp_dir):
    """Test PDF metadata extraction."""
    pdf_path = os.path.join(temp_dir, "sample.pdf")
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_metadata({"/Title": "Sample Title"})
    with open(pdf_path, "wb") as f:
        writer.write(f)
    
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract_pdf_metadata(pdf_path)
    
    assert meta.get("Pages") == 1
    assert meta.get("Title") == "Sample Title"


def test_extract_pdf_metadata_missing_file():
    """Test PDF extraction with missing file."""
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract_pdf_metadata("/nonexistent/file.pdf")
    
    assert "Error" in meta
    assert "File not found" in meta["Error"]


def test_extract_auto_detects_pdf(temp_dir):
    """Test that extract() auto-detects PDF files."""
    pdf_path = os.path.join(temp_dir, "sample.pdf")
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_metadata({"/Title": "Auto Detect"})
    with open(pdf_path, "wb") as f:
        writer.write(f)
    
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract(pdf_path)
    
    assert "Pages" in meta


def test_extract_auto_detects_text(temp_dir):
    """Test that extract() auto-detects text files."""
    test_file = os.path.join(temp_dir, "sample.py")
    with open(test_file, "w") as f:
        f.write("# Python code\nprint('hello')\n")
    
    extractor_obj = MetadataExtractor()
    meta = extractor_obj.extract(test_file)
    
    assert "Line Count" in meta
    assert "Encoding" in meta


def test_extract_handles_missing_file():
    """Test extract() with missing file."""
    meta = extract("missing-file-does-not-exist.xyz")
    
    assert "Error" in meta
    assert "File not found" in meta["Error"]


def test_extract_and_store(temp_dir):
    """Test extract and store functionality."""
    test_file = os.path.join(temp_dir, "sample.txt")
    with open(test_file, "w") as f:
        f.write("test content\nline 2\n")
    
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    meta, db_row = extractor_obj.extract_and_store(test_file)
    
    assert "Line Count" in meta
    assert db_row is not None
    assert len(db_client.saved) == 1


def test_extract_and_store_with_error(temp_dir):
    """Test extract and store with extraction failure."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    meta, db_row = extractor_obj.extract_and_store("/nonexistent/file.txt")
    
    assert "Error" in meta
    assert db_row is None


def test_batch_extract_reports_success_and_failure(temp_dir):
    """Test batch extraction with success and failure."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    good = os.path.join(temp_dir, "good.txt")
    with open(good, "w") as f:
        f.write("hello\nworld\n")
    
    missing = os.path.join(temp_dir, "missing.txt")
    
    progress_messages = []
    
    result = extractor_obj.batch_extract(
        [good, missing],
        progress_callback=lambda message, progress: progress_messages.append((message, progress)),
    )
    
    assert result["successful"] == 1
    assert result["failed"] == 1
    assert result["total"] == 2
    assert len(db_client.saved) == 1
    assert any("Processing" in msg[0] for msg in progress_messages)


def test_batch_extract_with_all_success(temp_dir):
    """Test batch extraction with all files succeeding."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    file1 = os.path.join(temp_dir, "file1.txt")
    file2 = os.path.join(temp_dir, "file2.txt")
    
    with open(file1, "w") as f:
        f.write("content1\n")
    with open(file2, "w") as f:
        f.write("content2\n")
    
    result = extractor_obj.batch_extract([file1, file2])
    
    assert result["successful"] == 2
    assert result["failed"] == 0
    assert result["total"] == 2


def test_batch_extract_with_no_files(temp_dir):
    """Test batch extraction with no files."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    result = extractor_obj.batch_extract([])
    
    assert result["successful"] == 0
    assert result["failed"] == 0
    assert result["total"] == 0


def test_batch_extract_progress_callback_exception(temp_dir):
    """Test batch extraction handles progress callback exceptions."""
    db_client = DummyDB()
    extractor_obj = MetadataExtractor(db_client=db_client)
    
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("test\n")
    
    def bad_callback(msg, progress):
        raise Exception("Callback failed")
    
    # Should not raise, just disable the callback
    result = extractor_obj.batch_extract([test_file], progress_callback=bad_callback)
    assert result["successful"] == 1


def test_wrapper_functions(temp_dir):
    """Test module-level wrapper functions."""
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("hello\nworld\n")
    
    # Test extract wrapper
    result = extract(test_file)
    assert "Line Count" in result
    
    # Test batch_extract wrapper
    batch_result = batch_extract([test_file])
    assert batch_result["total"] == 1
