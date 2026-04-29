"""
Icon Loader Module

Supports SVG/PNG, theme color management, development-time color/size adjustment
"""

from pathlib import Path
from typing import Optional
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QSize


def get_icon_color_for_theme() -> str:
    """
    Get icon color for current theme

    Returns:
        Hex color code
    """
    try:
        from managers.theme_manager import get_theme_manager

        tm = get_theme_manager()
        return tm.get_icon_color()
    except Exception as e:
        # Fallback to dark theme color if theme manager not available
        # (e.g., during initial import or circular dependency)
        return "#e0e0e0"


class IconLoader:
    """Icon loading and management class"""

    # === Development adjustment parameters (finalize before production) ===
    ICON_FORMAT = "svg"  # "svg" or "png"
    DEFAULT_SIZE = 64  # Default icon size (px)

    # Icon color definitions per theme
    THEME_COLORS = {
        "dark": "#e0e0e0",  # Dark mode: light gray (same as text)
        "light": "#000000",  # Light mode: black
    }

    # === Debug use only (development only) ===
    COLOR_OVERRIDE: Optional[str] = None  # Force color (None=disabled)
    SCALE_FACTOR: float = 1.0  # Temporary size adjustment multiplier

    # === Icon filename definitions ===
    ICON_NAMES = {
        "menu": "menu.svg",
        "folder": "folder.svg",
        "trash": "clear_all.svg",
        "delete": "delete.svg",
        "play": "play.svg",
        "pause": "pause.svg",
        "play_circle": "play_circle.svg",
        "pause_circle": "pause_circle.svg",
        "back": "arrow_back.svg",
        "settings": "settings.svg",
        "info": "info.svg",
        "save": "save.svg",
        "close": "close.svg",
        "image": "image.svg",
        "file_open": "file_open.svg",
        # Add more as needed
    }

    _icons_dir: Optional[Path] = None

    @classmethod
    def _get_icons_dir(cls) -> Path:
        """Get icon directory path"""
        if cls._icons_dir is None:
            # Relative path from main.py
            cls._icons_dir = Path(__file__).parent.parent / "icons"
        return cls._icons_dir

    @classmethod
    def _load_svg(cls, svg_path: Path, size: int, color: str) -> QIcon:
        """Load SVG file and convert to QIcon (apply color and size)"""
        # Load SVG content and replace color
        svg_content = svg_path.read_text(encoding="utf-8")

        # Replace fill attribute with specified color
        if color:
            # Replace existing fill attribute (fill="#..." or fill='...')
            import re

            svg_content = re.sub(r'fill="[^"]*"', f'fill="{color}"', svg_content)
            svg_content = re.sub(r"fill='[^']*'", f"fill='{color}'", svg_content)

        # Create SVG renderer (with color-replaced SVG)
        renderer = QSvgRenderer()
        renderer.load(svg_content.encode("utf-8"))

        # Create pixmap
        pixmap = QPixmap(QSize(size, size))
        pixmap.fill(Qt.transparent)

        # Render SVG
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

    @classmethod
    def _load_png(cls, name: str, theme: str, size: int) -> QIcon:
        """Load PNG file"""
        icons_dir = cls._get_icons_dir()
        png_path = icons_dir / theme / f"{name}_{size}.png"

        if not png_path.exists():
            # Fallback: default size
            png_path = icons_dir / theme / f"{name}_{cls.DEFAULT_SIZE}.png"

        if not png_path.exists():
            return QIcon()

        return QIcon(str(png_path))

    @classmethod
    def load(
        cls, name: str, size: Optional[int] = None, color: Optional[str] = None
    ) -> QIcon:
        """
        Load icon (generic method)

        Args:
            name: Icon name (key from ICON_NAMES or filename without extension)
            size: Icon size (None=DEFAULT_SIZE)
            color: Icon color (None=auto-detect from theme, SVG only)

        Returns:
            QIcon
        """
        size = size or cls.DEFAULT_SIZE
        size = int(size * cls.SCALE_FACTOR)

        # Debug color override
        if cls.COLOR_OVERRIDE:
            color = cls.COLOR_OVERRIDE
        # Auto-detect color from theme if not specified
        elif color is None:
            color = get_icon_color_for_theme()

        if cls.ICON_FORMAT == "svg":
            # Load SVG
            icons_dir = cls._get_icons_dir()
            svg_filename = cls.ICON_NAMES.get(name, f"{name}.svg")
            svg_path = icons_dir / svg_filename

            if not svg_path.exists():
                return QIcon()

            return cls._load_svg(svg_path, size, color)

        else:
            # Load PNG (default to dark since theme is unknown)
            return cls._load_png(name, "dark", size)

    @classmethod
    def load_themed(
        cls, name: str, theme: str = "dark", size: Optional[int] = None
    ) -> QIcon:
        """
        Load icon with theme-specific color (deprecated - use load() instead)

        Args:
            name: Icon name
            theme: Theme name ("dark" or "light")
            size: Icon size (None=DEFAULT_SIZE)

        Returns:
            QIcon
        """
        size = size or cls.DEFAULT_SIZE
        color = cls.THEME_COLORS.get(theme, cls.THEME_COLORS["dark"])

        if cls.ICON_FORMAT == "svg":
            return cls.load(name, size, color)
        else:
            return cls._load_png(name, theme, size)

    @classmethod
    def set_debug_color(cls, color: Optional[str]):
        """Debug: Force all icons to specified color"""
        cls.COLOR_OVERRIDE = color

    @classmethod
    def set_scale_factor(cls, factor: float):
        """Debug: Set icon size multiplier"""
        cls.SCALE_FACTOR = factor
