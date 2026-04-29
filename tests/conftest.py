"""
Test configuration and shared fixtures
"""

import pytest
from pathlib import Path
from PIL import Image
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample RGB image (100x100)"""
    img_path = temp_dir / "test_image.png"
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_rgba_image(temp_dir: Path) -> Path:
    """Create a sample RGBA image with transparency (100x100)"""
    img_path = temp_dir / "test_image_rgba.png"
    img = Image.new("RGBA", (100, 100), color=(0, 255, 0, 128))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_large_image(temp_dir: Path) -> Path:
    """Create a large image (2000x1500)"""
    img_path = temp_dir / "test_large.png"
    img = Image.new("RGB", (2000, 1500), color=(0, 0, 255))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_small_image(temp_dir: Path) -> Path:
    """Create a small image (10x10)"""
    img_path = temp_dir / "test_small.png"
    img = Image.new("RGB", (10, 10), color=(255, 255, 0))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_landscape_image(temp_dir: Path) -> Path:
    """Create a landscape image (200x100)"""
    img_path = temp_dir / "test_landscape.png"
    img = Image.new("RGB", (200, 100), color=(128, 128, 128))
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_portrait_image(temp_dir: Path) -> Path:
    """Create a portrait image (100x200)"""
    img_path = temp_dir / "test_portrait.png"
    img = Image.new("RGB", (100, 200), color=(64, 64, 64))
    img.save(img_path)
    return img_path


@pytest.fixture
def corrupted_image(temp_dir: Path) -> Path:
    """Create a corrupted image file"""
    img_path = temp_dir / "corrupted.png"
    img_path.write_bytes(b"Not a real image file")
    return img_path


@pytest.fixture
def non_image_file(temp_dir: Path) -> Path:
    """Create a non-image file"""
    file_path = temp_dir / "test.txt"
    file_path.write_text("This is not an image")
    return file_path
