# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-06-12

### Changed

- About dialog link now points to the official website (landing page) instead of the GitHub repository
  - The repository, issues, and license remain reachable from the website
- About dialog link label is now localized (Japanese: 公式サイト / English: Official Website) and follows language switching

## [1.2.0] - 2026-06-12

### Added

- Transparency fill option for alpha-capable formats (PNG / WebP / TGA)
  - New "Transparency Fill" section in the settings screen: fill color picker plus per-format checkboxes
  - When enabled, transparent areas are composited onto the configured fill color (useful for white-background product images, documents, ML datasets, etc.)
- TGA RLE compression option in the format panel (default: off / uncompressed)

### Changed

- TGA alpha control moved from the format panel to the settings screen "Transparency Fill" section
  - Existing `tga_alpha` setting is migrated automatically (inverted to `tga_flatten`)
- TGA output now uses 24-bit RGB for palette images without transparency (previously always 32-bit RGBA when alpha was enabled)
- BMP output now composites transparent areas onto the fill color, unified with JPG/TGA behavior (previously the alpha channel was simply dropped, exposing hidden colors); palette/grayscale images without transparency are still saved as 8-bit
- Generalized the fill color setting label (was described as JPG-only)

### Fixed

- Settings screen values were not applied during conversion:
  - Fill color was hardcoded to white regardless of the configured color
  - "Keep metadata" was always off
  - "When file exists: Overwrite" was always treated as "save with numbering suffix"

## [1.1.1] - 2026-06-10

### Fixed

- Locked the UI during conversion so that only the pause button and the window close button remain operational
  - Disabled the menu, add files, add folder, and clear all buttons while converting
  - Blocked drag & drop and the file list context menu while converting
  - Previously these controls (including "Clear all") were still active during conversion, which could disrupt an in-progress batch

### Changed

- Reset the progress bar to its initial state when the file list changes (add / remove / clear all)
  - The progress bar no longer stays full (green) after a completed conversion once the file list is modified
  - Reset is suppressed while a conversion is running

## [1.1.0] - 2026-05-25

### Added

- Added TGA (Truevision) format support for both input and output
- Added alpha channel toggle option for TGA output (include/exclude alpha)
- Auto bit-depth selection: 32-bit (RGBA) when alpha is included, 24-bit (RGB) when excluded

## [1.0.3] - 2026-05-13

### Added

- Added SVG splash screen at startup
- Positioned splash screen dynamically to the monitor where the cursor is located

## [1.0.2] - 2026-04-30

### Added

- Added NoScrollComboBox and NoScrollSlider custom widgets to prevent accidental changes via mouse wheel
- Added toolbar drag functionality to move window by dragging empty space on toolbar
  - 5-pixel drag threshold to prevent accidental window movement
  - Works only on empty toolbar space, buttons remain clickable

### Changed

- Changed build format from onefile to onedir for faster startup (2 seconds → 0.9 seconds on SSD)
- Reduced UI font size from 18px to 16px for better balance
- Adjusted button and menu padding from 14px 20px to 12px 18px
- Updated system requirements: disk space 100MB → 150MB

## [1.0.1] - 2026-04-30

### Added

- Added Windows version info resource (displays version 1.0.1 in exe properties)
- Added custom About dialog with unified design, GitHub link, and license information

### Fixed

- Fixed QComboBox dropdown arrow icon not displaying in exe build
- Fixed QComboBox dropdown arrow icon color not adapting to theme (Light/Dark)
- Fixed settings.json saved to incorrect location in exe build (now saves to portable data/ folder)
- Fixed QSS icon paths not resolving correctly in PyInstaller exe environment

### Changed

- Optimized exe build size from 251MB to 53MB by removing unnecessary dependencies
- Settings and theme-generated files now stored in data/ folder for better organization
- Arrow icon SVG files now generated at runtime with theme-appropriate colors
- Updated About dialog to match other dialogs' design style
- Simplified version display in main window from "Version 1.0.0 (PySide6)" to "v1.0.1"

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

[1.2.1]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.2.1
[1.2.0]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.2.0
[1.1.1]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.1.1
[1.1.0]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.1.0
[1.0.3]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.0.3
[1.0.2]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.0.2
[1.0.1]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.0.1
[1.0.0]: https://github.com/Amatsukast/SB-Image-Converter/releases/tag/v1.0.0
