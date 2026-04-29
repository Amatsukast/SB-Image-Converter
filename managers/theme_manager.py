"""
Theme Manager

Centralized theme management for the application.
Provides dynamic theme switching capabilities.
"""

import sys
from pathlib import Path
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QGuiApplication, QPalette
from PySide6.QtWidgets import QApplication
from config.constants import THEME_SYSTEM, THEME_DARK, THEME_LIGHT


class ThemeManager(QObject):
    """
    Theme manager for application-wide theme control

    Manages current theme and applies QSS stylesheets dynamically.
    """

    # Signal emitted when theme changes
    theme_changed = Signal(str)  # new theme code

    _instance = None

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize theme manager"""
        if self._initialized:
            return

        super().__init__()
        self._current_theme = THEME_DARK  # Default theme
        self._styles_dir = Path(__file__).parent.parent / "gui" / "styles"
        self._initialized = True

    @property
    def current_theme(self) -> str:
        """Get current theme code"""
        return self._current_theme

    def _detect_system_theme(self) -> str:
        """
        Detect system theme (dark or light)

        Returns:
            Theme code (THEME_DARK or THEME_LIGHT)
        """
        app = QGuiApplication.instance()
        if app:
            palette = app.palette()
            window_color = palette.color(QPalette.Window)

            # Calculate luminance to determine if background is dark or light
            # Using relative luminance formula
            luminance = (
                0.299 * window_color.red()
                + 0.587 * window_color.green()
                + 0.114 * window_color.blue()
            )

            # If luminance is low, it's a dark theme
            if luminance < 128:
                return THEME_DARK
            else:
                return THEME_LIGHT

        # Fallback to dark theme if app is not available
        return THEME_DARK

    def _load_qss(self, theme_code: str) -> str:
        """
        Load QSS stylesheet for the given theme

        Args:
            theme_code: Theme code (THEME_DARK or THEME_LIGHT)

        Returns:
            QSS stylesheet content
        """
        if theme_code == THEME_DARK:
            qss_file = self._styles_dir / "dark_theme.qss"
        elif theme_code == THEME_LIGHT:
            qss_file = self._styles_dir / "light_theme.qss"
        else:
            qss_file = self._styles_dir / "dark_theme.qss"  # Fallback

        if qss_file.exists():
            qss_content = qss_file.read_text(encoding="utf-8")

            # Fix icon paths for exe (frozen) execution
            if getattr(sys, "frozen", False):
                # PyInstaller extracts resources to sys._MEIPASS temporary folder
                base_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
                icons_path = base_path / "icons"
            else:
                # Running as script
                base_path = Path(__file__).parent.parent
                icons_path = base_path / "icons"

            # Replace relative paths with absolute paths (use forward slashes for Qt)
            icons_path_str = str(icons_path).replace("\\", "/")
            qss_content = qss_content.replace("url(icons/", f"url({icons_path_str}/")

            # Fix SVG icon colors in QSS to match theme
            # Replace hardcoded #e3e3e3 in arrow_drop_down.svg with theme color
            icon_color = self.get_icon_color()
            arrow_svg_path = icons_path / "arrow_drop_down.svg"
            if arrow_svg_path.exists():
                import re

                arrow_svg_content = arrow_svg_path.read_text(encoding="utf-8")
                # Replace fill color
                arrow_svg_content = re.sub(
                    r'fill="[^"]*"', f'fill="{icon_color}"', arrow_svg_content
                )

                # Write colored SVG to data folder (portable, consistent with settings.json)
                if getattr(sys, 'frozen', False):
                    # exe: save to data folder next to exe
                    data_dir = Path(sys.executable).parent / "data"
                else:
                    # script: save to data folder in project
                    data_dir = base_path / "data"

                data_dir.mkdir(parents=True, exist_ok=True)
                temp_arrow_path = data_dir / f"arrow_drop_down_{theme_code}.svg"
                temp_arrow_path.write_text(arrow_svg_content, encoding="utf-8")

                # Update QSS to use colored version
                temp_arrow_str = str(temp_arrow_path).replace("\\", "/")
                qss_content = qss_content.replace(
                    f"{icons_path_str}/arrow_drop_down.svg", temp_arrow_str
                )

            return qss_content
        else:
            return ""

    def set_theme(self, theme_code: str) -> None:
        """
        Set current theme and apply it immediately

        Args:
            theme_code: Theme code (THEME_SYSTEM, THEME_DARK, or THEME_LIGHT)
        """
        # If "system", detect actual system theme
        if theme_code == THEME_SYSTEM:
            actual_theme = self._detect_system_theme()
        else:
            actual_theme = theme_code

        # Validate theme code
        if actual_theme not in [THEME_DARK, THEME_LIGHT]:
            return

        # Update current theme BEFORE applying QSS
        # (so IconLoader can get correct color immediately)
        old_theme = self._current_theme
        self._current_theme = actual_theme

        # Load and apply QSS
        qss = self._load_qss(actual_theme)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)

        # Emit signal if theme changed
        if old_theme != actual_theme:
            self.theme_changed.emit(actual_theme)

    def get_icon_color(self) -> str:
        """
        Get icon color for current theme

        Returns:
            Hex color code for icons
        """
        if self._current_theme == THEME_LIGHT:
            return "#6c757d"  # Medium gray for light theme
        else:
            return "#b0b0b0"  # Lighter gray for dark theme

    def get_text_color(self) -> str:
        """
        Get text color for current theme

        Returns:
            Hex color code for text
        """
        if self._current_theme == THEME_LIGHT:
            return "#495057"  # Body text for light theme
        else:
            return "#e0e0e0"  # Body text for dark theme

    def get_background_color(self) -> str:
        """
        Get background color for current theme

        Returns:
            Hex color code for background
        """
        if self._current_theme == THEME_LIGHT:
            return "#f8f9fa"  # Base background for light theme
        else:
            return "#121212"  # Base background for dark theme

    def get_placeholder_color(self) -> str:
        """
        Get placeholder color for current theme

        Returns:
            Hex color code for placeholder text/icons
        """
        if self._current_theme == THEME_LIGHT:
            return "#adb5bd"  # Placeholder gray for light theme
        else:
            return "#616161"  # Placeholder gray for dark theme

    def get_heading_color(self) -> str:
        """
        Get heading/title color for current theme (High Emphasis)

        Returns:
            Hex color code for headings
        """
        if self._current_theme == THEME_LIGHT:
            return "#212529"  # Dark charcoal for light theme
        else:
            return "#f8f9fa"  # Off-white for dark theme

    def get_surface_color(self) -> str:
        """
        Get surface color for current theme (cards, dialogs, elevated UI)

        Returns:
            Hex color code for surface elements
        """
        if self._current_theme == THEME_LIGHT:
            return "#ffffff"  # Pure white for light theme
        else:
            return "#1e1e1e"  # Surface 1 for dark theme

    def get_surface2_color(self) -> str:
        """
        Get secondary surface color for current theme (hover, popups)

        Returns:
            Hex color code for elevated surface elements
        """
        if self._current_theme == THEME_LIGHT:
            return "#e9ecef"  # Light gray for light theme
        else:
            return "#2c2c2c"  # Surface 2 for dark theme


# Global singleton instance
_theme_manager = None


def get_theme_manager() -> ThemeManager:
    """
    Get global theme manager instance

    Returns:
        ThemeManager singleton
    """
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
