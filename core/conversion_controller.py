"""
Conversion Controller Module

Controls conversion process, progress tracking, and error handling (GUI-independent)
"""

from pathlib import Path
from typing import List, Dict, Optional
import time
from PySide6.QtCore import QObject, Signal
from core.output_path_resolver import OutputPathResolver
from core.image_processor import ImageProcessor
from managers.settings_manager import AppSettings
from config.constants import (
    RESIZE_MODE_RATIO,
    RESIZE_MODE_PIXELS,
    RESIZE_MODE_LONG_EDGE,
    RESIZE_MODE_SHORT_EDGE,
    STATUS_PENDING,
    STATUS_SUCCESS,
    STATUS_ERROR,
)
from config.translations import get_resize_mode_from_display
from managers.translation_manager import get_translation_manager


class ConversionController(QObject):
    """Conversion controller class (Logic layer)"""

    # Signal definitions
    progress_updated = Signal(int, int)  # (current, total)
    conversion_started = Signal()  # Conversion started
    conversion_completed = Signal(dict)  # Conversion completed (summary)
    file_processed = Signal(str, bool, str)  # (filename, success, message)
    error_occurred = Signal(str)  # Error occurred

    def __init__(self):
        super().__init__()
        self.tm = get_translation_manager()
        self.output_resolver = OutputPathResolver()
        self.image_processor = ImageProcessor()
        self._is_running = False
        self._is_paused = False
        self._is_stopped = False

    def start_conversion(self, file_list: List[Dict], settings: Dict) -> None:
        """
        Start conversion process

        Args:
            file_list: File list (from FileManager)
            settings: Settings (from SettingsPanel)
        """
        if self._is_running:
            return

        if not file_list:
            self.error_occurred.emit(self.tm.tr("notify.no_files_to_convert"))
            return

        self._is_running = True
        self._is_paused = False
        self._is_stopped = False

        # Apply settings
        self._apply_settings(settings)

        # Conversion start notification
        self.conversion_started.emit()

        # Execute conversion
        summary = self._process_files(file_list, settings)

        # Completion notification
        self._is_running = False
        self.conversion_completed.emit(summary)

    def _apply_settings(self, settings: Dict) -> None:
        """Apply settings"""
        # Output path settings
        output_path = settings.get("output_path", "./converted/")
        self.output_resolver.set_output_template(output_path)

        # Overwrite mode (default: False, to be implemented in settings screen)
        overwrite = settings.get("overwrite", False)
        self.output_resolver.set_overwrite_mode(overwrite)

    def _process_files(self, file_list: List[Dict], settings: Dict) -> Dict:
        """
        Process files in batch

        Args:
            file_list: File list
            settings: Settings

        Returns:
            dict: Summary
        """
        total = len(file_list)
        success_count = 0
        error_count = 0
        total_size_before = 0
        total_size_after = 0

        for i, file_data in enumerate(file_list):
            # Wait while paused
            while self._is_paused and not self._is_stopped:
                time.sleep(0.1)

            # Break loop if stopped
            if self._is_stopped:
                break

            # Update progress (just before processing)
            self.progress_updated.emit(i + 1, total)

            # Process file
            input_path = Path(file_data["path"])
            result = self._process_single_file(input_path, settings)

            if result["success"]:
                success_count += 1
                total_size_before += result["size_before"]
                total_size_after += result["size_after"]
                self.file_processed.emit(
                    input_path.name,
                    True,
                    f"{self.tm.tr('file_status.success')} ({result['size_before']} → {result['size_after']})",
                )
            else:
                error_count += 1
                error_msg = result.get(
                    "error", self.tm.tr("error.generic", message="Unknown")
                )
                self.file_processed.emit(input_path.name, False, error_msg)
                self.error_occurred.emit(f"{input_path.name}: {error_msg}")

        # Calculate cancelled count
        cancelled = total - success_count - error_count if self._is_stopped else 0

        return {
            "total": total,
            "success": success_count,
            "error": error_count,
            "cancelled": cancelled,
            "size_before": total_size_before,
            "size_after": total_size_after,
            "size_reduced": total_size_before - total_size_after,
        }

    def _process_single_file(self, input_path: Path, settings: Dict) -> Dict:
        """
        Process a single file

        Args:
            input_path: Input file path
            settings: Settings

        Returns:
            dict: Result
        """
        try:
            # Resolve output path
            output_format = settings["format"]
            output_path = self.output_resolver.resolve_output_path(
                input_path, output_format
            )

            # Create output folder
            success, error = self.output_resolver.ensure_output_folder(output_path)
            if not success:
                return {"success": False, "error": error}

            # Convert to AppSettings format
            app_settings = self._convert_to_app_settings(settings)

            # Execute image conversion
            result = self.image_processor.process(input_path, output_path, app_settings)

            if result["success"]:
                return {
                    "success": True,
                    "size_before": result["original_size"],
                    "size_after": result["output_size"],
                }
            else:
                return {
                    "success": False,
                    "error": result.get(
                        "error", self.tm.tr("error.generic", message="Unknown")
                    ),
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _convert_to_app_settings(self, settings: Dict) -> AppSettings:
        """
        Convert SettingsPanel settings to AppSettings format

        Args:
            settings: Settings dict from SettingsPanel

        Returns:
            AppSettings: Converted settings
        """
        app_settings = AppSettings()

        # Output format
        app_settings.output_format = settings.get("format", "WebP")

        # WebP settings
        app_settings.webp_quality = settings.get("webp_quality", 90)

        # PNG settings
        app_settings.png_compress_level = settings.get("png_compress", 4)

        # JPG settings
        app_settings.jpg_quality = settings.get("jpg_quality", 90)
        app_settings.jpg_subsampling = settings.get("jpg_subsample", "4:2:2")
        app_settings.jpg_progressive = settings.get("jpg_progressive", False)

        # Resize settings
        app_settings.resize_enabled = settings.get("resize_enabled", False)
        if app_settings.resize_enabled:
            mode = settings.get("resize_mode", RESIZE_MODE_RATIO)
            # Convert display name to constant if needed
            if mode not in (
                RESIZE_MODE_RATIO,
                RESIZE_MODE_PIXELS,
                RESIZE_MODE_LONG_EDGE,
                RESIZE_MODE_SHORT_EDGE,
            ):
                mode = get_resize_mode_from_display(mode)
            app_settings.resize_mode = mode
            if mode == RESIZE_MODE_RATIO:
                app_settings.resize_percentage = settings.get("resize_percent", 100)
            elif mode == RESIZE_MODE_PIXELS:
                app_settings.resize_px_width = settings.get("resize_width", 1920)
                app_settings.resize_px_height = settings.get("resize_height", 1080)
            elif mode in (RESIZE_MODE_LONG_EDGE, RESIZE_MODE_SHORT_EDGE):
                if mode == RESIZE_MODE_LONG_EDGE:
                    app_settings.resize_edge_value = settings.get("resize_long", 1920)
                else:
                    app_settings.resize_edge_value = settings.get("resize_short", 1080)

        # Output path
        app_settings.output_path = settings.get("output_path", "./converted/")

        # Other settings (using default values, configurable in future settings screen)
        app_settings.keep_metadata = False
        app_settings.transparent_bg_color = "#FFFFFF"

        return app_settings

    def pause(self) -> None:
        """Pause conversion"""
        self._is_paused = True

    def resume(self) -> None:
        """Resume conversion"""
        self._is_paused = False

    def stop(self) -> None:
        """Stop conversion"""
        self._is_stopped = True
        self._is_paused = False

    def is_running(self) -> bool:
        """Check if conversion is running"""
        return self._is_running
