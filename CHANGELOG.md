# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-30

### Added
- Initial release of SB Image Converter
- Batch image conversion with drag & drop support
- Format support: WebP, PNG, JPG, BMP
- 4 resize modes: Percentage, Fixed pixels, Long edge, Short edge
- Quality control for each format
  - WebP: Quality slider (0-100), compression method (0-6)
  - PNG: Compression level (0-9), optimization option
  - JPG: Quality slider (0-100), subsampling options, progressive mode
- Metadata management (keep or remove EXIF data)
- Dark and Light theme support
- Multi-language UI (English and Japanese)
- Smart output path resolver with automatic numbering
- Settings persistence across sessions
- Real-time conversion progress display
- Pause/resume functionality for batch processing
- Context menu for file list management
- Comprehensive unit tests (49 tests, 97% coverage for validators)

[1.0.0]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.0.0
