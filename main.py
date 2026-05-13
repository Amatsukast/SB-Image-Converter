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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap, QPainter, QCursor
from PySide6.QtSvg import QSvgRenderer
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

    # Show splash screen
    splash = None
    svg_path = Path(__file__).parent / "app-icon.svg"
    if svg_path.exists():
        # Render SVG to a QPixmap for crisp display at any scale
        splash_size = 500
        splash_pixmap = QPixmap(splash_size, splash_size)
        splash_pixmap.fill(Qt.transparent)

        renderer = QSvgRenderer(str(svg_path))
        painter = QPainter(splash_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        renderer.render(painter)
        painter.end()

        # Get the screen where the mouse cursor is currently located
        current_screen = app.screenAt(QCursor.pos())
        if current_screen:
            splash = QSplashScreen(
                current_screen, splash_pixmap, Qt.WindowStaysOnTopHint
            )
        else:
            splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)

        splash.setAttribute(Qt.WA_TranslucentBackground)
        splash.show()
        app.processEvents()

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

    if splash:
        splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
