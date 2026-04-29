from PIL import Image
from pathlib import Path
from managers.settings_manager import AppSettings
from config.constants import (
    RESIZE_MODE_RATIO,
    RESIZE_MODE_PIXELS,
    RESIZE_MODE_LONG_EDGE,
    RESIZE_MODE_SHORT_EDGE,
)
from config.translations import translate


class ImageProcessor:
    def __init__(self):
        self.supported_formats = {
            ".webp": "WEBP",
            ".png": "PNG",
            ".jpg": "JPEG",
            ".jpeg": "JPEG",
            ".bmp": "BMP",
        }

    def process(
        self, input_path: Path, output_path: Path, settings: AppSettings
    ) -> dict:
        """
        画像を変換処理する

        Returns:
            dict: {
                'success': bool,
                'error': str (失敗時),
                'original_size': int,
                'output_size': int,
                'reduction': int (削減サイズ)
            }
        """
        try:
            with Image.open(input_path) as img:
                original_size = input_path.stat().st_size

                if settings.resize_enabled:
                    img = self.resize_image(img, settings)

                output_path.parent.mkdir(parents=True, exist_ok=True)

                self.save_image(img, output_path, settings)

                output_size = output_path.stat().st_size
                reduction = original_size - output_size

                return {
                    "success": True,
                    "original_size": original_size,
                    "output_size": output_size,
                    "reduction": reduction,
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def resize_image(self, img: Image.Image, settings: AppSettings) -> Image.Image:
        """Resize processing"""
        mode = settings.resize_mode
        original_width, original_height = img.size

        if mode == RESIZE_MODE_RATIO:
            scale = settings.resize_percentage / 100.0
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

        elif mode == RESIZE_MODE_PIXELS:
            new_width = settings.resize_px_width
            new_height = settings.resize_px_height

        elif mode == RESIZE_MODE_LONG_EDGE:
            target = settings.resize_edge_value
            if original_width >= original_height:
                scale = target / original_width
            else:
                scale = target / original_height
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

        elif mode == RESIZE_MODE_SHORT_EDGE:
            target = settings.resize_edge_value
            if original_width <= original_height:
                scale = target / original_width
            else:
                scale = target / original_height
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

        else:
            return img

        if new_width <= 0 or new_height <= 0:
            return img

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def save_image(
        self, img: Image.Image, output_path: Path, settings: AppSettings
    ) -> None:
        """Save image by format"""
        output_format = settings.output_format.upper()

        if output_format == "WEBP":
            self.save_as_webp(img, output_path, settings)
        elif output_format == "PNG":
            self.save_as_png(img, output_path, settings)
        elif output_format == "JPG":
            self.save_as_jpg(img, output_path, settings)
        elif output_format == "BMP":
            self.save_as_bmp(img, output_path, settings)
        else:
            raise ValueError(
                translate("error.unsupported_format_processing", format=output_format)
            )

    def save_as_webp(
        self, img: Image.Image, output_path: Path, settings: AppSettings
    ) -> None:
        """Save as WebP format"""
        quality = settings.webp_quality
        lossless = quality == 100

        save_kwargs = {
            "format": "WEBP",
            "lossless": lossless,
            "method": settings.webp_method,
        }

        if not lossless:
            save_kwargs["quality"] = quality

        if not settings.keep_metadata:
            save_kwargs["exif"] = b""

        img.save(output_path, **save_kwargs)

    def save_as_png(
        self, img: Image.Image, output_path: Path, settings: AppSettings
    ) -> None:
        """Save as PNG format"""
        compress_level = max(0, min(9, settings.png_compress_level))

        save_kwargs = {
            "format": "PNG",
            "compress_level": compress_level,
            "optimize": settings.png_optimize,
        }

        if not settings.keep_metadata:
            save_kwargs["exif"] = b""

        img.save(output_path, **save_kwargs)

    def save_as_jpg(
        self, img: Image.Image, output_path: Path, settings: AppSettings
    ) -> None:
        """Save as JPG format"""
        if img.mode in ("RGBA", "LA", "P"):
            bg_color = self.hex_to_rgb(settings.transparent_bg_color)
            background = Image.new("RGB", img.size, bg_color)
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        quality = max(0, min(100, settings.jpg_quality))

        subsampling_map = {"4:4:4": 0, "4:2:2": 2, "4:2:0": 2}
        subsampling = subsampling_map.get(settings.jpg_subsampling, 2)

        save_kwargs = {
            "format": "JPEG",
            "quality": quality,
            "subsampling": subsampling,
            "progressive": settings.jpg_progressive,
        }

        if not settings.keep_metadata:
            save_kwargs["exif"] = b""

        img.save(output_path, **save_kwargs)

    def save_as_bmp(
        self, img: Image.Image, output_path: Path, settings: AppSettings
    ) -> None:
        """Save as BMP format"""
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.save(output_path, format="BMP")

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color code to RGB tuple"""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
