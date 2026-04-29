"""
Tests for core.image_processor module (resize functionality only)
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
