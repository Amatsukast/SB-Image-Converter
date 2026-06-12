"""
Tests for core.image_processor module (resize and alpha flattening)
"""

import pytest
from pathlib import Path
from PIL import Image
from core.image_processor import ImageProcessor
from managers.settings_manager import AppSettings
from config.constants import (
    RESIZE_MODE_RATIO,
    RESIZE_MODE_PIXELS,
    RESIZE_MODE_LONG_EDGE,
    RESIZE_MODE_SHORT_EDGE,
)


@pytest.fixture
def processor():
    """Create ImageProcessor instance"""
    return ImageProcessor()


@pytest.fixture
def default_settings():
    """Create default AppSettings"""
    return AppSettings()


class TestResizeImagePercentage:
    """Tests for resize_image with percentage mode"""

    def test_resize_50_percent(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """Resize to 50% should halve dimensions"""
        with Image.open(sample_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_RATIO
            default_settings.resize_percentage = 50

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (50, 50)

    def test_resize_200_percent(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """Resize to 200% should double dimensions"""
        with Image.open(sample_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_RATIO
            default_settings.resize_percentage = 200

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (200, 200)

    def test_resize_100_percent(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """Resize to 100% should maintain dimensions"""
        with Image.open(sample_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_RATIO
            default_settings.resize_percentage = 100

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (100, 100)


class TestResizeImagePixels:
    """Tests for resize_image with pixel mode"""

    def test_resize_to_specific_dimensions(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """Resize to specific pixel dimensions"""
        with Image.open(sample_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_PIXELS
            default_settings.resize_px_width = 200
            default_settings.resize_px_height = 150

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (200, 150)

    def test_resize_to_square(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_landscape_image: Path,
    ):
        """Resize non-square image to square"""
        with Image.open(sample_landscape_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_PIXELS
            default_settings.resize_px_width = 100
            default_settings.resize_px_height = 100

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (100, 100)


class TestResizeImageLongEdge:
    """Tests for resize_image with long edge mode"""

    def test_resize_landscape_long_edge(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_landscape_image: Path,
    ):
        """Resize landscape image by long edge (width)"""
        with Image.open(sample_landscape_image) as img:
            # Original: 200x100
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_LONG_EDGE
            default_settings.resize_edge_value = 100

            resized = processor.resize_image(img, default_settings)

            # Long edge (200) resized to 100, short edge scaled proportionally
            assert resized.size == (100, 50)

    def test_resize_portrait_long_edge(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_portrait_image: Path,
    ):
        """Resize portrait image by long edge (height)"""
        with Image.open(sample_portrait_image) as img:
            # Original: 100x200
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_LONG_EDGE
            default_settings.resize_edge_value = 100

            resized = processor.resize_image(img, default_settings)

            # Long edge (200) resized to 100, short edge scaled proportionally
            assert resized.size == (50, 100)

    def test_resize_square_long_edge(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """Resize square image by long edge"""
        with Image.open(sample_image) as img:
            # Original: 100x100
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_LONG_EDGE
            default_settings.resize_edge_value = 50

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (50, 50)


class TestResizeImageShortEdge:
    """Tests for resize_image with short edge mode"""

    def test_resize_landscape_short_edge(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_landscape_image: Path,
    ):
        """Resize landscape image by short edge (height)"""
        with Image.open(sample_landscape_image) as img:
            # Original: 200x100
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_SHORT_EDGE
            default_settings.resize_edge_value = 50

            resized = processor.resize_image(img, default_settings)

            # Short edge (100) resized to 50, long edge scaled proportionally
            assert resized.size == (100, 50)

    def test_resize_portrait_short_edge(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_portrait_image: Path,
    ):
        """Resize portrait image by short edge (width)"""
        with Image.open(sample_portrait_image) as img:
            # Original: 100x200
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_SHORT_EDGE
            default_settings.resize_edge_value = 50

            resized = processor.resize_image(img, default_settings)

            # Short edge (100) resized to 50, long edge scaled proportionally
            assert resized.size == (50, 100)


class TestResizeEdgeCases:
    """Tests for edge cases in resize functionality"""

    def test_resize_very_small_image(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_small_image: Path,
    ):
        """Resize very small image (10x10)"""
        with Image.open(sample_small_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_RATIO
            default_settings.resize_percentage = 50

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (5, 5)

    def test_resize_large_image(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_large_image: Path,
    ):
        """Resize large image (2000x1500)"""
        with Image.open(sample_large_image) as img:
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_LONG_EDGE
            default_settings.resize_edge_value = 1000

            resized = processor.resize_image(img, default_settings)

            assert resized.size == (1000, 750)

    def test_resize_disabled(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """When resize is disabled, image should remain unchanged"""
        with Image.open(sample_image) as img:
            original_size = img.size
            default_settings.resize_enabled = False

            result = processor.resize_image(img, default_settings)

            assert result.size == original_size

    def test_zero_dimension_fallback(
        self,
        processor: ImageProcessor,
        default_settings: AppSettings,
        sample_image: Path,
    ):
        """When calculated dimension is 0 or negative, return original"""
        with Image.open(sample_image) as img:
            original_size = img.size
            default_settings.resize_enabled = True
            default_settings.resize_mode = RESIZE_MODE_PIXELS
            default_settings.resize_px_width = 0
            default_settings.resize_px_height = 0

            result = processor.resize_image(img, default_settings)

            # Should return original image when dimensions are invalid
            assert result.size == original_size


@pytest.fixture
def green_bg_settings():
    """AppSettings with green transparent background color"""
    settings = AppSettings()
    settings.transparent_bg_color = "#00FF00"
    return settings


def _transparent_rgba() -> Image.Image:
    """Fully transparent red RGBA image (10x10)"""
    return Image.new("RGBA", (10, 10), (255, 0, 0, 0))


def _transparent_palette() -> Image.Image:
    """Palette image (10x10) whose only used index is transparent"""
    img = Image.new("P", (10, 10), color=1)
    img.putpalette([0, 0, 255, 255, 0, 0] + [0, 0, 0] * 254)
    img.info["transparency"] = 1
    return img


def _opaque_palette() -> Image.Image:
    """Palette image (10x10) without transparency info"""
    img = Image.new("P", (10, 10), color=0)
    img.putpalette([0, 0, 255] + [0, 0, 0] * 255)
    return img


class TestFlattenAlpha:
    """Tests for flatten_alpha (transparency compositing onto background color)"""

    def test_transparent_rgba_filled_with_bg_color(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """Fully transparent RGBA pixels become the background color"""
        result = processor.flatten_alpha(_transparent_rgba(), green_bg_settings)

        assert result.mode == "RGB"
        assert result.getpixel((5, 5)) == (0, 255, 0)

    def test_opaque_rgba_keeps_original_colors(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """Opaque RGBA pixels keep their colors after flattening"""
        img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))

        result = processor.flatten_alpha(img, green_bg_settings)

        assert result.mode == "RGB"
        assert result.getpixel((5, 5)) == (255, 0, 0)

    def test_transparent_palette_filled_with_bg_color(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """Palette image with transparency info is composited onto bg color"""
        result = processor.flatten_alpha(_transparent_palette(), green_bg_settings)

        assert result.mode == "RGB"
        assert result.getpixel((5, 5)) == (0, 255, 0)

    def test_opaque_palette_returned_unchanged(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """Palette image without transparency info is returned as-is"""
        img = _opaque_palette()

        result = processor.flatten_alpha(img, green_bg_settings)

        assert result is img
        assert result.mode == "P"

    def test_rgb_returned_unchanged(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """RGB image (no alpha) is returned as-is"""
        img = Image.new("RGB", (10, 10), (1, 2, 3))

        result = processor.flatten_alpha(img, green_bg_settings)

        assert result is img

    def test_la_filled_with_bg_color(
        self, processor: ImageProcessor, green_bg_settings: AppSettings
    ):
        """Fully transparent LA pixels become the background color"""
        img = Image.new("LA", (10, 10), (200, 0))

        result = processor.flatten_alpha(img, green_bg_settings)

        assert result.mode == "RGB"
        assert result.getpixel((5, 5)) == (0, 255, 0)


class TestSaveAlphaHandling:
    """Tests for per-format alpha handling on save (JPG/BMP/TGA unified)"""

    def test_bmp_transparent_filled_with_bg_color(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """BMP: transparent area is filled with the configured bg color"""
        output = temp_dir / "out.bmp"

        processor.save_as_bmp(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGB"
            assert saved.getpixel((5, 5)) == (0, 255, 0)

    def test_bmp_opaque_palette_stays_8bit(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """BMP: palette image without transparency stays palette (8-bit)"""
        output = temp_dir / "out.bmp"

        processor.save_as_bmp(_opaque_palette(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "P"

    def test_jpg_transparent_filled_with_bg_color(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """JPG: transparent area is filled with the configured bg color"""
        output = temp_dir / "out.jpg"

        processor.save_as_jpg(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            r, g, b = saved.getpixel((5, 5))
            # JPEG is lossy: allow small tolerance
            assert abs(r - 0) <= 8 and abs(g - 255) <= 8 and abs(b - 0) <= 8

    def test_tga_flatten_transparent_filled_with_bg_color(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (flatten on): transparent area is filled with the configured bg color"""
        output = temp_dir / "out.tga"
        green_bg_settings.tga_flatten = True

        processor.save_as_tga(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGB"
            assert saved.getpixel((5, 5)) == (0, 255, 0)

    def test_tga_no_flatten_preserves_transparency(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (flatten off): transparency is preserved as RGBA"""
        output = temp_dir / "out.tga"
        green_bg_settings.tga_flatten = False

        processor.save_as_tga(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGBA"
            assert saved.getpixel((5, 5))[3] == 0

    def test_tga_no_flatten_opaque_palette_saved_as_rgb(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (flatten off): palette without transparency is saved as RGB (24-bit)"""
        output = temp_dir / "out.tga"
        green_bg_settings.tga_flatten = False

        processor.save_as_tga(_opaque_palette(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGB"
            assert saved.getpixel((5, 5)) == (0, 0, 255)

    def test_tga_no_flatten_transparent_palette_saved_as_rgba(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (flatten off): palette with transparency is saved as RGBA (32-bit)"""
        output = temp_dir / "out.tga"
        green_bg_settings.tga_flatten = False

        processor.save_as_tga(_transparent_palette(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGBA"
            assert saved.getpixel((5, 5))[3] == 0

    def test_png_flatten_transparent_filled_with_bg_color(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """PNG (flatten on): transparent area is filled with the configured bg color"""
        output = temp_dir / "out.png"
        green_bg_settings.png_flatten = True

        processor.save_as_png(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGB"
            assert saved.getpixel((5, 5)) == (0, 255, 0)

    def test_png_no_flatten_preserves_transparency(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """PNG (flatten off, default): transparency is preserved"""
        output = temp_dir / "out.png"

        processor.save_as_png(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.mode == "RGBA"
            assert saved.getpixel((5, 5))[3] == 0

    def test_webp_flatten_transparent_filled_with_bg_color(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """WebP (flatten on): transparent area is filled with the configured bg color"""
        output = temp_dir / "out.webp"
        green_bg_settings.webp_flatten = True
        green_bg_settings.webp_quality = 100  # lossless for exact pixel match

        processor.save_as_webp(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.getpixel((5, 5))[:3] == (0, 255, 0)

    def test_webp_no_flatten_preserves_transparency(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """WebP (flatten off, default): transparency is preserved"""
        output = temp_dir / "out.webp"
        green_bg_settings.webp_quality = 100

        processor.save_as_webp(_transparent_rgba(), output, green_bg_settings)

        with Image.open(output) as saved:
            saved = saved.convert("RGBA")
            assert saved.getpixel((5, 5))[3] == 0

    def test_tga_rle_compression(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (RLE on): file is RLE-compressed and pixels are intact"""
        output = temp_dir / "out_rle.tga"
        green_bg_settings.tga_rle = True
        img = Image.new("RGB", (100, 100), (255, 0, 0))

        processor.save_as_tga(img, output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.info.get("compression") == "tga_rle"
            assert saved.getpixel((50, 50)) == (255, 0, 0)

    def test_tga_no_rle_by_default(
        self,
        processor: ImageProcessor,
        green_bg_settings: AppSettings,
        temp_dir: Path,
    ):
        """TGA (RLE off, default): file is uncompressed"""
        output = temp_dir / "out_raw.tga"
        img = Image.new("RGB", (100, 100), (255, 0, 0))

        processor.save_as_tga(img, output, green_bg_settings)

        with Image.open(output) as saved:
            assert saved.info.get("compression") != "tga_rle"
            assert saved.getpixel((50, 50)) == (255, 0, 0)
