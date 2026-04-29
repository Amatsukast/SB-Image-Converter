"""
Validation Module

File format detection, settings validation, image file checking
"""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image
from config.translations import translate


class Validators:
    """Validation class"""

    # 対応フォーマット
    SUPPORTED_FORMATS = {".webp", ".png", ".jpg", ".jpeg", ".bmp"}

    # 出力フォーマット
    OUTPUT_FORMATS = {"WebP", "PNG", "JPG", "BMP"}

    @classmethod
    def is_supported_format(cls, file_path: Path) -> bool:
        """
        対応フォーマットかどうかを判定

        Args:
            file_path: ファイルパス

        Returns:
            bool: 対応フォーマットならTrue
        """
        return file_path.suffix.lower() in cls.SUPPORTED_FORMATS

    @classmethod
    def is_image_file(cls, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        画像ファイルとして有効かチェック

        Args:
            file_path: ファイルパス

        Returns:
            Tuple[bool, Optional[str]]: (有効かどうか, エラーメッセージ)
        """
        if not file_path.exists():
            return False, translate("error.file_not_exist")

        if not file_path.is_file():
            return False, translate("error.not_a_file")

        if not cls.is_supported_format(file_path):
            return False, translate("error.unsupported_format", suffix=file_path.suffix)

        # Pillowで開けるかチェック（破損検出）
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True, None
        except Exception as e:
            return False, translate("error.image_corrupted", detail=str(e))

    @classmethod
    def validate_quality(
        cls, quality: int, format_name: str
    ) -> Tuple[bool, Optional[str]]:
        """
        品質値のバリデーション

        Args:
            quality: 品質値
            format_name: フォーマット名（"WebP", "PNG", "JPG", "BMP"）

        Returns:
            Tuple[bool, Optional[str]]: (有効かどうか, エラーメッセージ)
        """
        if format_name in ("WebP", "JPG"):
            if not 0 <= quality <= 100:
                return False, translate("error.quality_range", format=format_name)
        elif format_name == "PNG":
            if not 0 <= quality <= 9:
                return False, translate("error.png_compress_range")
        # BMPは品質設定なし
        return True, None

    @classmethod
    def validate_resize_value(cls, value: int, mode: str) -> Tuple[bool, Optional[str]]:
        """
        リサイズ値のバリデーション

        Args:
            value: リサイズ値
            mode: モード（"px", "percent", "long", "short"）

        Returns:
            Tuple[bool, Optional[str]]: (有効かどうか, エラーメッセージ)
        """
        if value <= 0:
            return False, translate("error.resize_value_min")

        if mode == "percent":
            if value > 500:
                return False, translate("error.percentage_max")
        elif mode in ("px", "long", "short"):
            if value > 50000:
                return False, translate("error.pixel_max")

        return True, None

    @classmethod
    def validate_output_path(cls, path_str: str) -> Tuple[bool, Optional[str]]:
        """
        出力先パスのバリデーション

        Args:
            path_str: パス文字列

        Returns:
            Tuple[bool, Optional[str]]: (有効かどうか, エラーメッセージ)
        """
        if not path_str or not path_str.strip():
            return False, translate("error.output_path_empty")

        # 相対パス表記は許可
        if path_str.strip() in ("./converted/", "./converted", "converted"):
            return True, None

        # 絶対パスの場合、親ディレクトリが存在するかチェック
        try:
            path = Path(path_str)
            if path.is_absolute():
                if not path.parent.exists():
                    return False, translate("error.output_parent_not_exist")
            return True, None
        except Exception as e:
            return False, translate("error.invalid_path", detail=str(e))

    @classmethod
    def get_image_info(cls, file_path: Path) -> Optional[dict]:
        """
        画像ファイルの情報を取得

        Args:
            file_path: ファイルパス

        Returns:
            dict or None: {width, height, format, size, mode} or None（エラー時）
        """
        try:
            with Image.open(file_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "size": file_path.stat().st_size,
                    "mode": img.mode,
                }
        except (OSError, IOError):
            return None
