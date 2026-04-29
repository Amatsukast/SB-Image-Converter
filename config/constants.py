"""
Application constants

Internal constant values used in logic layer.
All UI-facing text is handled separately in translations.py.
"""

# Output formats (internal values)
FORMAT_WEBP = "WebP"
FORMAT_PNG = "PNG"
FORMAT_JPG = "JPG"
FORMAT_BMP = "BMP"

# Resize modes (internal values)
RESIZE_MODE_RATIO = "ratio"
RESIZE_MODE_PIXELS = "pixels"
RESIZE_MODE_LONG_EDGE = "long_edge"
RESIZE_MODE_SHORT_EDGE = "short_edge"

# File statuses
STATUS_PENDING = "pending"
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

# JPG subsampling options
JPG_SUBSAMPLING_444 = "4:4:4"
JPG_SUBSAMPLING_422 = "4:2:2"
JPG_SUBSAMPLING_420 = "4:2:0"

# Theme options
THEME_SYSTEM = "system"
THEME_DARK = "dark"
THEME_LIGHT = "light"

# Language options
LANG_SYSTEM = "system"
LANG_JAPANESE = "ja"
LANG_ENGLISH = "en"

# Default values
DEFAULT_OUTPUT_PATH = "./converted/"
DEFAULT_LANGUAGE = LANG_SYSTEM
DEFAULT_THEME = THEME_SYSTEM
