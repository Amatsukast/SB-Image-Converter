"""
SB Image Converter

Copyright (C) 2026 Amatsukast

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow
from managers.settings_manager import SettingsManager
from managers.translation_manager import get_translation_manager
from managers.theme_manager import get_theme_manager


def main() -> None:
    """Application startup"""
    # High DPI support (automatically enabled in Qt 6)
    # Removed deprecated settings from Qt 6.11

    app = QApplication(sys.argv)
    app.setApplicationName("SB Image Converter")
    app.setOrganizationName("SB Tools")

    # Set application icon
    icon_path = Path(__file__).parent / "app_icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Load settings
    settings_manager = SettingsManager()

    # Apply language
    tm = get_translation_manager()
    tm.set_language(settings_manager.settings.language)

    # Apply theme
    theme_manager = get_theme_manager()
    theme_manager.set_theme(settings_manager.settings.theme)

    # Show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
