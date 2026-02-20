import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from risk_analyzer import PrivacyForensicAnalyzer, analyze_metadata, analyze_batch


def test_analyze_metadata_high_risk_with_reasons():
    metadata = {
        "GPS Latitude": "28.6139",
        "GPS Longitude": "77.2090",
        "Author": "Alice",
        "Camera Model": "iPhone 15",
        "Software": "Photoshop > Lightroom",
        "XMP Block": "present",
        "CreateDate": "2025-01-10 12:00:00",
        "ModifyDate": "2025-01-08 10:00:00",
    }
    result = analyze_metadata(metadata, "C:/tmp/photo.jpg")

    assert result["risk_level"] in {"MEDIUM", "HIGH"}
    assert result["risk_score"] >= 60
    assert len(result["reasons"]) > 0
    assert isinstance(result["timeline"], list)


def test_analyze_metadata_low_risk():
    metadata = {
        "Line Count": 10,
        "Encoding": "utf-8",
    }
    analyzer = PrivacyForensicAnalyzer()
    result = analyzer.analyze_file(metadata, "C:/tmp/readme.txt")

    assert result["risk_level"] == "LOW"
    assert result["risk_score"] < 30


def test_analyze_batch_summary_and_folders():
    entries = [
        {"file_path": "C:/A/file1.jpg", "metadata": {"GPS": "12.1,77.2", "Author": "User A"}},
        {"file_path": "C:/A/file2.txt", "metadata": {"Line Count": 8}},
        {"file_path": "C:/B/file3.pdf", "metadata": {"Producer": "Acrobat", "CreationDate": "2024-01-01"}},
    ]

    summary = analyze_batch(entries)

    assert summary["total_files"] == 3
    assert "risk_counts" in summary
    assert "folders" in summary
    assert "C:/A" in summary["folders"]
    assert "C:/B" in summary["folders"]
    assert isinstance(summary["results"], list)


def test_timeline_uses_fallback_timestamps_when_metadata_has_no_dates():
    analyzer = PrivacyForensicAnalyzer()
    metadata = {"Author": "NoDate User"}
    fallback = {
        "Created Date": "2025-01-01 08:00:00",
        "Modified Date": "2025-01-02 09:00:00",
        "Extraction Date": "2025-01-03 10:00:00",
    }

    result = analyzer.analyze_file(metadata, "C:/tmp/file.txt", fallback_timestamps=fallback)

    assert len(result["timeline"]) == 3
    assert result["timeline"][0]["event"] == "Created Date"
    assert result["timeline"][1]["event"] == "Modified Date"
    assert result["timeline"][2]["event"] == "Extraction Date"
