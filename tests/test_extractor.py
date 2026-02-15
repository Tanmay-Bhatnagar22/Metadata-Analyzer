import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import extractor
from PyPDF2 import PdfWriter


class DummyDB:
    """In-memory stub used to capture insert calls."""

    def __init__(self):
        self.saved = []

    def insert_metadata(self, file_path, metadata):
        entry = {"file_path": str(file_path), "metadata": metadata}
        self.saved.append(entry)
        return entry


def test_extract_text_metadata(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("first line\nsecond line\n", encoding="utf-8")

    meta = extractor.MetadataExtractor().extract_text_metadata(str(sample))

    assert meta["Line Count"] == 2
    assert meta["Encoding"] == "utf-8"
    assert meta["File Size (bytes)"] > 0


def test_extract_pdf_metadata(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_metadata({"/Title": "Sample Title"})
    with open(pdf_path, "wb") as f:
        writer.write(f)

    meta = extractor.MetadataExtractor().extract_pdf_metadata(str(pdf_path))

    assert meta.get("Pages") == 1
    assert meta.get("Title") == "Sample Title"


def test_extract_handles_missing_file():
    meta = extractor.extract("missing-file-does-not-exist.xyz")

    assert "Error" in meta
    assert "File not found" in meta["Error"]


def test_batch_extract_reports_success_and_failure(tmp_path):
    db_client = DummyDB()
    extractor_instance = extractor.MetadataExtractor(db_client=db_client)

    good = tmp_path / "good.txt"
    good.write_text("hello\nworld\n", encoding="utf-8")
    missing = tmp_path / "missing.txt"

    progress_messages = []

    result = extractor_instance.batch_extract(
        [str(good), str(missing)],
        progress_callback=lambda message, progress: progress_messages.append(message),
    )

    assert result["successful"] == 1
    assert result["failed"] == 1
    assert result["total"] == 2
    assert len(db_client.saved) == 1
    assert db_client.saved[0]["file_path"] == str(good)
    assert any("Processing" in msg for msg in progress_messages)
