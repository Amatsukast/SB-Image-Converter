"""
Tests for core.validators module
"""

import pytest
from pathlib import Path
from core.validators import Validators


class TestIsSupportedFormat:
    """Tests for is_supported_format method"""

    def test_webp_format(self):
        """WebP format should be supported"""
        assert Validators.is_supported_format(Path("test.webp")) is True

    def test_png_format(self):
        """PNG format should be supported"""
        assert Validators.is_supported_format(Path("test.png")) is True

    def test_jpg_format(self):
        """JPG format should be supported"""
        assert Validators.is_supported_format(Path("test.jpg")) is True

    def test_jpeg_format(self):
        """JPEG format should be supported"""
        assert Validators.is_supported_format(Path("test.jpeg")) is True

    def test_bmp_format(self):
        """BMP format should be supported"""
        assert Validators.is_supported_format(Path("test.bmp")) is True

    def test_case_insensitive(self):
        """Format check should be case-insensitive"""
        assert Validators.is_supported_format(Path("test.PNG")) is True
        assert Validators.is_supported_format(Path("test.JPG")) is True
        assert Validators.is_supported_format(Path("test.WEBP")) is True

    def test_unsupported_format(self):
        """Unsupported formats should return False"""
        assert Validators.is_supported_format(Path("test.gif")) is False
        assert Validators.is_supported_format(Path("test.txt")) is False
        assert Validators.is_supported_format(Path("test.pdf")) is False


class TestIsImageFile:
    """Tests for is_image_file method"""

    def test_valid_image(self, sample_image: Path):
        """Valid image should pass"""
        is_valid, error = Validators.is_image_file(sample_image)
        assert is_valid is True
        assert error is None

    def test_non_existent_file(self, temp_dir: Path):
        """Non-existent file should fail"""
        non_existent = temp_dir / "does_not_exist.png"
        is_valid, error = Validators.is_image_file(non_existent)
        assert is_valid is False
        assert error is not None

    def test_directory_as_file(self, temp_dir: Path):
        """Directory path should fail"""
        is_valid, error = Validators.is_image_file(temp_dir)
        assert is_valid is False
        assert error is not None

    def test_unsupported_format_file(self, non_image_file: Path):
        """File with unsupported extension should fail"""
        is_valid, error = Validators.is_image_file(non_image_file)
        assert is_valid is False
        assert error is not None

    def test_corrupted_image(self, corrupted_image: Path):
        """Corrupted image file should fail"""
        is_valid, error = Validators.is_image_file(corrupted_image)
        assert is_valid is False
        assert error is not None

    def test_rgba_image(self, sample_rgba_image: Path):
        """RGBA image should be valid"""
        is_valid, error = Validators.is_image_file(sample_rgba_image)
        assert is_valid is True
        assert error is None


class TestValidateQuality:
    """Tests for validate_quality method"""

    def test_webp_valid_quality(self):
        """WebP quality 0-100 should be valid"""
        assert Validators.validate_quality(0, "WebP")[0] is True
        assert Validators.validate_quality(50, "WebP")[0] is True
        assert Validators.validate_quality(100, "WebP")[0] is True

    def test_webp_invalid_quality(self):
        """WebP quality outside 0-100 should be invalid"""
        assert Validators.validate_quality(-1, "WebP")[0] is False
        assert Validators.validate_quality(101, "WebP")[0] is False

    def test_jpg_valid_quality(self):
        """JPG quality 0-100 should be valid"""
        assert Validators.validate_quality(0, "JPG")[0] is True
        assert Validators.validate_quality(75, "JPG")[0] is True
        assert Validators.validate_quality(100, "JPG")[0] is True

    def test_jpg_invalid_quality(self):
        """JPG quality outside 0-100 should be invalid"""
        assert Validators.validate_quality(-1, "JPG")[0] is False
        assert Validators.validate_quality(101, "JPG")[0] is False

    def test_png_valid_quality(self):
        """PNG compression 0-9 should be valid"""
        assert Validators.validate_quality(0, "PNG")[0] is True
        assert Validators.validate_quality(6, "PNG")[0] is True
        assert Validators.validate_quality(9, "PNG")[0] is True

    def test_png_invalid_quality(self):
        """PNG compression outside 0-9 should be invalid"""
        assert Validators.validate_quality(-1, "PNG")[0] is False
        assert Validators.validate_quality(10, "PNG")[0] is False

    def test_bmp_quality(self):
        """BMP format should accept any quality value"""
        assert Validators.validate_quality(0, "BMP")[0] is True
        assert Validators.validate_quality(100, "BMP")[0] is True
        assert Validators.validate_quality(999, "BMP")[0] is True


class TestValidateResizeValue:
    """Tests for validate_resize_value method"""

    def test_percent_valid_range(self):
        """Percentage 1-500 should be valid"""
        assert Validators.validate_resize_value(1, "percent")[0] is True
        assert Validators.validate_resize_value(100, "percent")[0] is True
        assert Validators.validate_resize_value(500, "percent")[0] is True

    def test_percent_invalid_range(self):
        """Percentage 0 or >500 should be invalid"""
        assert Validators.validate_resize_value(0, "percent")[0] is False
        assert Validators.validate_resize_value(-1, "percent")[0] is False
        assert Validators.validate_resize_value(501, "percent")[0] is False

    def test_px_valid_range(self):
        """Pixel value 1-50000 should be valid"""
        assert Validators.validate_resize_value(1, "px")[0] is True
        assert Validators.validate_resize_value(1920, "px")[0] is True
        assert Validators.validate_resize_value(50000, "px")[0] is True

    def test_px_invalid_range(self):
        """Pixel value 0 or >50000 should be invalid"""
        assert Validators.validate_resize_value(0, "px")[0] is False
        assert Validators.validate_resize_value(-1, "px")[0] is False
        assert Validators.validate_resize_value(50001, "px")[0] is False

    def test_long_edge_valid_range(self):
        """Long edge 1-50000 should be valid"""
        assert Validators.validate_resize_value(100, "long")[0] is True
        assert Validators.validate_resize_value(3840, "long")[0] is True
        assert Validators.validate_resize_value(50000, "long")[0] is True

    def test_short_edge_valid_range(self):
        """Short edge 1-50000 should be valid"""
        assert Validators.validate_resize_value(100, "short")[0] is True
        assert Validators.validate_resize_value(2160, "short")[0] is True
        assert Validators.validate_resize_value(50000, "short")[0] is True


class TestValidateOutputPath:
    """Tests for validate_output_path method"""

    def test_empty_path(self):
        """Empty path should be invalid"""
        assert Validators.validate_output_path("")[0] is False
        assert Validators.validate_output_path("   ")[0] is False

    def test_relative_path(self):
        """Relative path should be valid"""
        assert Validators.validate_output_path("./converted/")[0] is True
        assert Validators.validate_output_path("./converted")[0] is True
        assert Validators.validate_output_path("converted")[0] is True

    def test_absolute_path_valid(self, temp_dir: Path):
        """Absolute path with existing parent should be valid"""
        valid_path = str(temp_dir / "output")
        assert Validators.validate_output_path(valid_path)[0] is True

    def test_absolute_path_invalid(self):
        """Absolute path with non-existing parent should be invalid"""
        invalid_path = "C:/NonExistentParent123456/output"
        is_valid, error = Validators.validate_output_path(invalid_path)
        assert is_valid is False
        assert error is not None


class TestGetImageInfo:
    """Tests for get_image_info method"""

    def test_valid_image_info(self, sample_image: Path):
        """Valid image should return correct info"""
        info = Validators.get_image_info(sample_image)
        assert info is not None
        assert info["width"] == 100
        assert info["height"] == 100
        assert info["format"] == "PNG"
        assert info["size"] > 0
        assert "mode" in info

    def test_large_image_info(self, sample_large_image: Path):
        """Large image info should be correct"""
        info = Validators.get_image_info(sample_large_image)
        assert info is not None
        assert info["width"] == 2000
        assert info["height"] == 1500

    def test_rgba_image_info(self, sample_rgba_image: Path):
        """RGBA image should have correct mode"""
        info = Validators.get_image_info(sample_rgba_image)
        assert info is not None
        assert info["mode"] == "RGBA"

    def test_corrupted_image_info(self, corrupted_image: Path):
        """Corrupted image should return None"""
        info = Validators.get_image_info(corrupted_image)
        assert info is None

    def test_non_existent_image_info(self, temp_dir: Path):
        """Non-existent file should return None"""
        non_existent = temp_dir / "does_not_exist.png"
        info = Validators.get_image_info(non_existent)
        assert info is None
