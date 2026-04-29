import json
from pathlib import Path
from dataclasses import dataclass, asdict
from config.constants import (
    RESIZE_MODE_RATIO,
    DEFAULT_OUTPUT_PATH,
    DEFAULT_LANGUAGE,
    DEFAULT_THEME,
)


@dataclass
class AppSettings:
    # Output format settings
    output_format: str = "WebP"

    # WebP settings
    webp_quality: int = 90
    webp_method: int = 4

    # PNG settings
    png_compress_level: int = 4
    png_optimize: bool = False

    # JPG settings
    jpg_quality: int = 90
    jpg_subsampling: str = "4:2:2"
    jpg_progressive: bool = False

    # Resize settings
    resize_enabled: bool = False
    resize_mode: str = RESIZE_MODE_RATIO
    resize_percentage: int = 100
    resize_px_width: int = 1920
    resize_px_height: int = 1080
    resize_edge_value: int = 1920

    # Output path settings
    output_path: str = DEFAULT_OUTPUT_PATH
    numbering_enabled: bool = True

    # Other settings
    language: str = DEFAULT_LANGUAGE
    theme: str = DEFAULT_THEME
    recursive_folder: bool = False
    overwrite_mode: bool = False
    keep_metadata: bool = False
    transparent_bg_color: str = "#FFFFFF"


class SettingsManager:
    def __init__(self, settings_path: Path = None):
        if settings_path is None:
            settings_path = Path(__file__).parent.parent / "data" / "settings.json"
        self.settings_path = settings_path
        self.settings = self.load()

    def load(self) -> AppSettings:
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return AppSettings(**data)
            except (json.JSONDecodeError, FileNotFoundError, KeyError):
                return AppSettings()
        return AppSettings()

    def save(self, settings: AppSettings = None) -> None:
        if settings is None:
            settings = self.settings

        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(asdict(settings), f, ensure_ascii=False, indent=2)
        except (OSError, IOError):
            pass

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self.save()
