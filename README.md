# Metadata Analyzer

A comprehensive desktop application for extracting, editing, and managing file metadata with a modern graphical user interface. Built with Python and Tkinter, this tool supports multiple file formats and provides powerful features for metadata analysis and reporting.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## Overview

Metadata Analyzer is a feature-rich application designed to extract, view, edit, and export metadata from various file types. The application maintains a history of all metadata extractions in a SQLite database and provides advanced filtering, searching, and reporting capabilities.

## Key Features

### Metadata Extraction
- Extract metadata from multiple file formats:
  - **PDF files**: Title, Author, Subject, Creator, Producer, Keywords, page count
  - **Images**: EXIF data from JPEG, PNG, TIFF, BMP, GIF
  - **Audio files**: MP3, WAV, FLAC, M4A, OGG metadata
  - **Text files**: File size, line count, encoding details
  - **Office documents**: DOCX, XLSX, PPTX metadata
  - **Media files**: Video and audio metadata using Hachoir parser

### Metadata Editing
- Edit extracted metadata with an intuitive interface
- Add custom metadata fields dynamically
- Validate metadata before saving
- Write modified metadata back to source files
- Non-editable system fields (File Name, File Size, File Type, timestamps)

### Database Management
- SQLite database for persistent storage
- Automatic metadata versioning
- Track extraction history with timestamps
- Advanced search and filter capabilities
- Export functionality for data analysis

### Reporting & Visualization
- Generate comprehensive reports in multiple formats:
  - **PDF**: Professional formatted reports with tables and styling
  - **JSON**: Structured data export
  - **XML**: Standard XML format
  - **CSV**: Spreadsheet-compatible format
  - **Excel**: XLSX format with formatting
- Real-time report preview with zoom controls
- Print report functionality
- Visual statistics and analytics

### History Management
- View all extraction history in a tree view
- Search by filename or path
- Filter by file type (PDF, TXT, JPG, PNG, MP3, etc.)
- Date range filtering (Today, This Week, This Month, Last 30 Days)
- Multiple sorting options (Date, Name, Size)
- Delete individual records or clear entire history
- Export history data for analysis

### User Interface
- Modern flat design with professional styling
- Tabbed interface for organized workflow:
  - **Extractor Tab**: File selection and metadata extraction
  - **Editor Tab**: Metadata viewing and editing
  - **History Tab**: Search, filter, and manage extraction history
  - **Preview Tab**: Report generation and preview
- Progress indicators for long operations
- Status bar with real-time updates
- Keyboard shortcuts for common actions
- Responsive layout with scrollable content

## Project Structure

```
Metadata Analyser/
├── src/
│   ├── main.py          # Application entry point
│   ├── gui.py           # GUI implementation (Tkinter interface)
│   ├── extractor.py     # Metadata extraction logic
│   ├── editor.py        # Metadata editing and file writing
│   ├── db.py            # Database operations (SQLite)
│   ├── report.py        # Report generation (PDF, JSON, XML, CSV, Excel)
│   └── __pycache__/     # Python bytecode cache
├── tests/
│   ├── test_main.py     # Main module tests
│   ├── test_gui.py      # GUI component tests
│   ├── test_extractor.py # Extraction functionality tests
│   ├── test_editor.py   # Editor functionality tests
│   ├── test_db.py       # Database operation tests
│   ├── test_report.py   # Report generation tests
│   └── __pycache__/     # Test bytecode cache
├── requirements.txt     # Python dependencies
└── file_metadata.db     # SQLite database (created on first run)
```

## Technical Architecture

### Core Components

#### 1. MetadataExtractor (extractor.py)
Object-oriented metadata extractor supporting multiple file types:
- PDF extraction using PyPDF2
- Text file analysis with encoding detection
- Generic file metadata using Hachoir parser
- Batch extraction with progress callbacks
- Automatic format detection based on MIME types

#### 2. MetadataEditor (editor.py)
Handles metadata editing and file writing:
- Parse and validate metadata from text format
- Write metadata back to original files
- Format-specific writers for PDF, images, audio files
- Backup creation before writing
- Error handling and rollback on failure

#### 3. MetadataDatabase (db.py)
SQLite database wrapper for persistence:
- CRUD operations for metadata records
- Advanced filtering and searching
- Statistics calculation
- Data export in multiple formats
- Transaction management

#### 4. MetadataReporter (report.py)
Multi-format report generator:
- PDF reports with ReportLab (tables, styles, images)
- JSON/XML/CSV export
- Excel workbook generation with openpyxl
- Text-based report formatting
- Template-based report generation

#### 5. MetadataAnalyzerApp (gui.py)
Main GUI application class:
- Tkinter-based interface with modern styling
- Tab management for different workflows
- Event handling and user interactions
- Thread-safe operations for background tasks
- Image preview with zoom capabilities

## Requirements

### Core Dependencies
- Python 3.7 or higher
- PyPDF2 >= 3.0.0 - PDF manipulation
- Pillow >= 10.0.0 - Image processing
- pandas >= 2.0.0 - Data analysis
- reportlab >= 4.0.0 - PDF report generation
- hachoir >= 3.2.0 - Generic file parsing
- pdf2image >= 1.16.0 - PDF to image conversion
- matplotlib >= 3.7.0 - Visualization

### Optional Dependencies
- piexif >= 1.1.3 - Image EXIF metadata (JPEG, TIFF)
- mutagen >= 1.47.0 - Audio metadata (MP3, FLAC, M4A)
- python-docx >= 1.1.0 - Microsoft Word files
- openpyxl >= 3.1.0 - Excel file generation

### Test Dependencies
- pytest >= 8.3.0 - Testing framework

## Installation

### Step 1: Clone or Download the Project
```bash
git clone https://github.com/Tanmay-Bhatnagar22/Metadata-Analyzer.git
cd Metadata-Analyzer
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv .venv
```

Activate the virtual environment:
- **Windows**: `.venv\Scripts\activate`
- **Linux/Mac**: `source .venv/bin/activate`

### Step 3: Install Dependencies

**Install core dependencies only:**
```bash
pip install PyPDF2 Pillow pandas reportlab hachoir pdf2image matplotlib pytest
```

**Install all dependencies (including optional):**
```bash
pip install -r requirements.txt
```

**Install optional dependencies separately:**
```bash
# For enhanced metadata writing
pip install piexif mutagen python-docx openpyxl
```

## Usage

### Starting the Application

Run the application from the command line:
```bash
python src/main.py
```

Or from within Python:
```python
from src.gui import run_gui
run_gui()
```

### Basic Workflow

#### 1. Extract Metadata
1. Navigate to the **Extractor** tab
2. Click **Choose File** to select a file
3. Click **Extract** to extract metadata
4. View the extracted metadata in the display area

#### 2. Edit Metadata
1. After extraction, click **Editor** button
2. Switch to the **Editor** tab
3. Modify metadata fields (editable fields only)
4. Click **Add Metadata** to add custom fields
5. Click **Save Changes** to persist changes
6. Optionally, write changes back to file

#### 3. Generate Reports
1. Click **Generate Report** from Extractor or Editor tab
2. Switch to the **Preview** tab to view the report
3. Use zoom controls (+, -, Reset) to adjust preview
4. Click **Save Report** to export in desired format
5. Click **Print Report** to print the report

#### 4. View History
1. Navigate to the **History** tab
2. Use the search bar to find specific files
3. Apply filters (file type, date range)
4. Sort results using dropdown menu
5. Select records to view details or delete
6. Export history data for external analysis

### Keyboard Shortcuts

- **Ctrl+O**: Open file chooser
- **Ctrl+E**: Extract metadata
- **Ctrl+S**: Save editor changes
- **Ctrl+R**: Generate report
- **Ctrl+H**: Switch to History tab
- **Ctrl+Q**: Quit application

## Testing

The project includes comprehensive test coverage for all modules.

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Files
```bash
pytest tests/test_extractor.py
pytest tests/test_editor.py
pytest tests/test_db.py
pytest tests/test_report.py
pytest tests/test_gui.py
```

### Run Tests with Coverage
```bash
pytest --cov=src tests/
```

### Test Modules
- **test_extractor.py**: Tests for metadata extraction from various file types
- **test_editor.py**: Tests for metadata editing and file writing
- **test_db.py**: Tests for database operations and queries
- **test_report.py**: Tests for report generation in multiple formats
- **test_gui.py**: Tests for GUI components and interactions
- **test_main.py**: Tests for application entry point

## Supported File Types

### Fully Supported (Extract + Edit)
- **PDF**: .pdf
- **Images**: .jpg, .jpeg, .png, .tiff, .tif
- **Audio**: .mp3, .flac, .m4a

### Extract Only
- **Text files**: .txt, .py, .cpp, .c, .java, .js, .json, .csv, .md, .html, .css
- **Office documents**: .docx, .xlsx, .pptx
- **Video files**: .mp4, .avi, .mkv, .mov (via Hachoir)
- **Other media**: Various formats supported by Hachoir parser

## Database Schema

The SQLite database stores metadata with the following schema:

```sql
CREATE TABLE metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size_formatted TEXT,
    file_type TEXT,
    extracted_at TEXT NOT NULL,
    modified_on TEXT,
    full_metadata TEXT NOT NULL  -- JSON string
);
```

## Error Handling

The application includes comprehensive error handling:
- Validation of file paths and formats
- Graceful handling of unsupported file types
- Backup creation before modifying files
- Rollback on write failures
- User-friendly error messages
- Logging of exceptions for debugging

## Performance Considerations

- **Batch Processing**: Support for multiple files with progress tracking
- **Caching**: Statistics cache with 30-second TTL
- **Threading**: Background operations for UI responsiveness
- **Database Indexing**: Efficient queries with proper indexing
- **Memory Management**: Streaming for large files

## Future Enhancements

Potential areas for future development:
- Support for additional file formats
- Cloud storage integration
- Advanced metadata comparison tools
- Batch editing capabilities
- Command-line interface (CLI)
- Plugin system for custom extractors
- Metadata templates and presets
- Multi-language support

## Troubleshooting

### Common Issues

**Issue: "No module named 'tkinter'"**
- **Solution**: Install tkinter for your Python version
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`

**Issue: PDF preview not showing**
- **Solution**: Install poppler-utils for pdf2image
  - Windows: Download from poppler release page
  - Ubuntu: `sudo apt-get install poppler-utils`

**Issue: "Cannot write metadata to file"**
- **Solution**: Ensure file is not open in another application
- Check file permissions (read/write access)
- Verify optional dependencies are installed (piexif, mutagen)

**Issue: GUI not launching**
- **Solution**: Check for missing dependencies: `pip install -r requirements.txt`
- Ensure Metadata.png icon file exists in the root directory

## License

This project is licensed under the MIT License.

## Author

Developed as part of a metadata management solution for file organization and analysis.

## Contributing

Contributions are welcome. Please ensure:
- Code follows existing style conventions
- All tests pass before submitting
- New features include appropriate tests
- Documentation is updated accordingly

## Support

For issues, questions, or feature requests, please review the test files for usage examples or check the inline documentation in each module.
