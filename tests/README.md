# SB Image Converter - Unit Tests

## Overview

This directory contains unit tests for the SB Image Converter core modules.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── test_validators.py       # Tests for core/validators.py (35 tests)
└── test_image_processor.py  # Tests for core/image_processor.py resize (14 tests)
```

## Test Coverage

- **core/validators.py**: 97% coverage (65 statements, 63 covered)
- **core/image_processor.py**: 42% coverage (resize functionality only)

Total: 49 tests, 100% pass rate

## Running Tests

### Basic test run

```bash
pytest tests/
```

### Verbose output

```bash
pytest tests/ -v
```

### With coverage report

```bash
pytest tests/ --cov=core --cov-report=term
```

### Run specific test file

```bash
pytest tests/test_validators.py -v
pytest tests/test_image_processor.py -v
```

## Requirements

- pytest >= 7.0
- pytest-cov >= 3.0 (for coverage reports)
- Pillow >= 10.0

Install with:

```bash
pip install pytest pytest-cov Pillow
```

## Test Categories

### test_validators.py (35 tests)

#### TestIsSupportedFormat (7 tests)

- WebP, PNG, JPG, JPEG, BMP format detection
- Case-insensitive checking
- Unsupported format rejection

#### TestIsImageFile (6 tests)

- Valid image file verification
- Non-existent file detection
- Directory vs file distinction
- Corrupted image detection
- RGBA image support

#### TestValidateQuality (7 tests)

- WebP quality range (0-100)
- JPG quality range (0-100)
- PNG compression level (0-9)
- BMP format handling

#### TestValidateResizeValue (6 tests)

- Percentage mode (1-500%)
- Pixel mode (1-50000px)
- Long edge mode
- Short edge mode

#### TestValidateOutputPath (4 tests)

- Empty path rejection
- Relative path support
- Absolute path validation
- Parent directory existence check

#### TestGetImageInfo (5 tests)

- Image dimensions retrieval
- Format detection
- File size calculation
- Color mode detection

### test_image_processor.py (14 tests)

#### TestResizeImagePercentage (3 tests)

- 50% resize
- 200% resize
- 100% no-change resize

#### TestResizeImagePixels (2 tests)

- Specific dimension resize
- Non-square to square resize

#### TestResizeImageLongEdge (3 tests)

- Landscape image resize by long edge
- Portrait image resize by long edge
- Square image resize by long edge

#### TestResizeImageShortEdge (2 tests)

- Landscape image resize by short edge
- Portrait image resize by short edge

#### TestResizeEdgeCases (4 tests)

- Very small image (10x10)
- Large image (2000x1500)
- Resize disabled mode
- Zero dimension fallback

## Fixtures (conftest.py)

### Image Fixtures

- `sample_image`: 100x100 RGB image
- `sample_rgba_image`: 100x100 RGBA image with transparency
- `sample_large_image`: 2000x1500 RGB image
- `sample_small_image`: 10x10 RGB image
- `sample_landscape_image`: 200x100 RGB image
- `sample_portrait_image`: 100x200 RGB image

### Test File Fixtures

- `corrupted_image`: Invalid image data
- `non_image_file`: Text file with .txt extension

### Utility Fixtures

- `temp_dir`: Temporary directory for test files (auto-cleanup)

## Testing Strategy

### In Scope

- **Core validation logic**: All validation functions in validators.py
- **Resize algorithms**: All resize modes (percentage, pixel, long edge, short edge)
- **Edge cases**: Boundary values, invalid inputs, extreme dimensions

### Out of Scope

- **GUI components**: Manual testing sufficient for PyQt6 widgets
- **Image saving logic**: Format-specific options tested via integration tests
- **Manager classes**: Simple getters/setters don't require unit tests
- **Worker threads**: Tested via integration tests

## Notes

- Tests run in ~0.2 seconds (fast execution)
- All tests are isolated (use temporary directories)
- No external dependencies required (fixtures generate test images)
- Compatible with CI/CD pipelines
