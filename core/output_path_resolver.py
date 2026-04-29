"""
Output Path Resolver Module

Resolves output paths, generates sequential suffixes, creates folders
"""

from pathlib import Path
from typing import Tuple, Optional
from config.constants import DEFAULT_OUTPUT_PATH
from config.translations import translate


class OutputPathResolver:
    """Output path resolver class"""

    MAX_NUMBERING_ATTEMPTS = 10000  # Maximum attempts for sequential numbering

    def __init__(
        self, output_path_template: str = DEFAULT_OUTPUT_PATH, overwrite: bool = False
    ):
        """
        Args:
            output_path_template: 出力先パステンプレート
            overwrite: 上書きモード（True=上書き、False=連番サフィックス）
        """
        self.output_path_template = output_path_template
        self.overwrite = overwrite

    def resolve_output_path(self, input_file_path: Path, output_format: str) -> Path:
        """
        出力先パスを解決

        Args:
            input_file_path: 入力ファイルパス
            output_format: 出力フォーマット（"WebP", "PNG", "JPG", "BMP"）

        Returns:
            Path: 出力先パス
        """
        # 出力フォーマットに応じた拡張子
        ext_map = {
            "WebP": ".webp",
            "PNG": ".png",
            "JPG": ".jpg",
            "BMP": ".bmp",
        }
        output_ext = ext_map.get(output_format, ".png")

        # 出力先フォルダを決定
        output_folder = self._resolve_output_folder(input_file_path)

        # 出力ファイル名（拡張子を変更）
        output_filename = input_file_path.stem + output_ext

        # 出力先パス
        output_path = output_folder / output_filename

        # 上書きモードでない場合、連番サフィックスを付加
        if not self.overwrite and output_path.exists():
            output_path = self._add_number_suffix(output_path)

        return output_path

    def _resolve_output_folder(self, input_file_path: Path) -> Path:
        """
        出力先フォルダを解決

        Args:
            input_file_path: 入力ファイルパス

        Returns:
            Path: 出力先フォルダパス
        """
        template = self.output_path_template.strip()

        # デフォルト相対パス表記
        if template in ("./converted/", "./converted", "converted"):
            # 元ファイルと同じフォルダ内にconvertedサブフォルダ作成
            output_folder = input_file_path.parent / "converted"
        else:
            # カスタムパス指定
            output_folder = Path(template)

            # 相対パスの場合、元ファイルのフォルダを基準に
            if not output_folder.is_absolute():
                output_folder = input_file_path.parent / output_folder

        return output_folder

    def _add_number_suffix(self, file_path: Path) -> Path:
        """
        連番サフィックスを付加

        Args:
            file_path: ファイルパス

        Returns:
            Path: 連番サフィックス付きパス（例: image_1.jpg）
        """
        folder = file_path.parent
        stem = file_path.stem
        ext = file_path.suffix

        counter = 1
        while True:
            new_path = folder / f"{stem}_{counter}{ext}"
            if not new_path.exists():
                return new_path
            counter += 1

            # Prevent infinite loop
            if counter > self.MAX_NUMBERING_ATTEMPTS:
                raise RuntimeError(
                    translate("error.numbering_failed", file=str(file_path))
                )

    def ensure_output_folder(self, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        出力先フォルダが存在することを確認（なければ作成）

        Args:
            output_path: 出力先パス

        Returns:
            Tuple[bool, Optional[str]]: (成功, エラーメッセージ)
        """
        output_folder = output_path.parent

        if output_folder.exists():
            return True, None

        try:
            output_folder.mkdir(parents=True, exist_ok=True)
            return True, None
        except Exception as e:
            return False, translate("error.folder_creation_failed", detail=str(e))

    def set_output_template(self, template: str):
        """出力先テンプレートを設定"""
        self.output_path_template = template

    def set_overwrite_mode(self, overwrite: bool):
        """上書きモードを設定"""
        self.overwrite = overwrite
