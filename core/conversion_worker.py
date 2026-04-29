"""
Conversion Worker Module

Background processing using QThread
"""

from typing import List, Dict
from PySide6.QtCore import QThread, Signal
from core.conversion_controller import ConversionController
from managers.translation_manager import get_translation_manager


class ConversionWorker(QThread):
    """Conversion worker class (background execution)"""

    # Signal definitions
    progress_updated = Signal(int, int)  # (current, total)
    conversion_started = Signal()
    conversion_completed = Signal(dict)  # Summary
    file_processed = Signal(str, bool, str)  # (filename, success, message)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.tm = get_translation_manager()
        self.controller = ConversionController()
        self.file_list = []
        self.settings = {}

        # Connect controller signals to worker signals
        self.controller.progress_updated.connect(self.progress_updated.emit)
        self.controller.conversion_started.connect(self.conversion_started.emit)
        self.controller.conversion_completed.connect(self.conversion_completed.emit)
        self.controller.file_processed.connect(self.file_processed.emit)
        self.controller.error_occurred.connect(self.error_occurred.emit)

    def set_task(self, file_list: List[Dict], settings: Dict) -> None:
        """Set conversion task"""
        self.file_list = file_list
        self.settings = settings

    def run(self):
        """Thread execution (background)"""
        if not self.file_list:
            self.error_occurred.emit(self.tm.tr("notify.no_files_to_convert"))
            return

        # Execute conversion
        self.controller.start_conversion(self.file_list, self.settings)

    def pause(self) -> None:
        """Pause conversion"""
        self.controller.pause()

    def resume(self) -> None:
        """Resume conversion"""
        self.controller.resume()

    def stop(self) -> None:
        """Stop conversion"""
        self.controller.stop()

    def is_running_conversion(self) -> bool:
        """Check if conversion is running"""
        return self.controller.is_running()
