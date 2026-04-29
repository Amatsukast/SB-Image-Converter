"""
File List Management Module

File addition/removal, duplicate checking, sorting (GUI-independent)
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from PySide6.QtCore import QObject, Signal
from core.validators import Validators
from config.constants import STATUS_PENDING, STATUS_SUCCESS, STATUS_ERROR
from managers.translation_manager import get_translation_manager


class FileManager(QObject):
    """ファイルリスト管理クラス（Logic層）"""

    # シグナル定義
    list_updated = Signal(list)  # ファイルリスト更新時
    file_added = Signal(str, str)  # (ファイルパス, ステータス)
    error_occurred = Signal(str)  # エラー発生時
    status_message = Signal(str)  # ステータスメッセージ通知

    def __init__(self, recursive: bool = False):
        """
        Args:
            recursive: サブフォルダ再帰読み込み（デフォルト: False）
        """
        super().__init__()
        self.tm = get_translation_manager()
        self._files: List[Dict] = []  # ファイル情報リスト
        self._file_paths_set = set()  # 重複チェック用
        self.recursive = recursive

    def get_files(self) -> List[Dict]:
        """ファイルリストを取得"""
        return self._files.copy()

    def get_file_count(self) -> int:
        """ファイル数を取得"""
        return len(self._files)

    def add_files(self, paths: List[str], show_status: bool = True) -> None:
        """
        ファイルまたはフォルダを追加

        Args:
            paths: ファイル/フォルダパスのリスト
            show_status: ステータス通知を表示するか
        """
        added_count = 0
        skipped_count = 0
        error_count = 0

        for path_str in paths:
            path = Path(path_str)

            if path.is_file():
                result = self._add_single_file(path, show_status)
                if result == "added":
                    added_count += 1
                elif result == "skipped":
                    skipped_count += 1
                else:
                    error_count += 1

            elif path.is_dir():
                count = self._add_files_from_folder(path, show_status)
                added_count += count

        # ソート実行
        if added_count > 0:
            self._sort_files()
            self.list_updated.emit(self._files)

        # サマリー通知
        if show_status and (added_count > 0 or skipped_count > 0 or error_count > 0):
            summary = self.tm.tr("notify.files_added", count=added_count)
            if skipped_count > 0:
                summary += f" {self.tm.tr('notify.files_skipped', count=skipped_count)}"
            if error_count > 0:
                summary += f" {self.tm.tr('notify.files_error', count=error_count)}"
            self.status_message.emit(summary)

    def _add_single_file(self, file_path: Path, show_status: bool = True) -> str:
        """
        単一ファイルを追加

        Args:
            file_path: ファイルパス
            show_status: ステータス通知を表示するか

        Returns:
            str: "added", "skipped", "error"
        """
        # 重複チェック
        if str(file_path.resolve()) in self._file_paths_set:
            if show_status:
                self.file_added.emit(
                    str(file_path), self.tm.tr("file_status.already_added")
                )
            return "skipped"

        # フォーマットチェック
        if not Validators.is_supported_format(file_path):
            if show_status:
                self.file_added.emit(
                    str(file_path), self.tm.tr("file_status.unsupported")
                )
            return "error"

        # 画像ファイルチェック
        is_valid, error_msg = Validators.is_image_file(file_path)
        if not is_valid:
            if show_status:
                self.file_added.emit(
                    str(file_path), self.tm.tr("error.generic", message=error_msg)
                )
                self.error_occurred.emit(f"{file_path.name}: {error_msg}")
            return "error"

        # 画像情報取得
        info = Validators.get_image_info(file_path)
        if not info:
            if show_status:
                self.file_added.emit(
                    str(file_path), self.tm.tr("error.info_retrieval_failed")
                )
            return "error"

        # ファイル情報を追加
        file_data = {
            "path": str(file_path.resolve()),
            "name": file_path.name,
            "folder": str(file_path.parent),
            "size": info["size"],
            "width": info["width"],
            "height": info["height"],
            "format": info["format"],
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
            "status": STATUS_PENDING,  # pending / success / error
        }

        self._files.append(file_data)
        self._file_paths_set.add(str(file_path.resolve()))

        if show_status:
            self.file_added.emit(str(file_path), self.tm.tr("file_status.added"))

        return "added"

    def _add_files_from_folder(
        self, folder_path: Path, show_status: bool = True
    ) -> int:
        """
        フォルダ内のファイルを追加

        Args:
            folder_path: フォルダパス
            show_status: ステータス通知を表示するか

        Returns:
            int: 追加されたファイル数
        """
        added_count = 0

        if self.recursive:
            # 再帰的に取得
            pattern = "**/*"
        else:
            # 直下のみ
            pattern = "*"

        # 対応フォーマットのファイルを取得
        for ext in Validators.SUPPORTED_FORMATS:
            for file_path in folder_path.glob(f"{pattern}{ext}"):
                if file_path.is_file():
                    result = self._add_single_file(file_path, show_status=False)
                    if result == "added":
                        added_count += 1

        return added_count

    def _sort_files(self) -> None:
        """
        ファイルリストをソート

        ソート戦略:
        - 1件追加: 追加順（ソートしない）
        - 複数件一括追加: 名前順
        - 複数フォルダ: パス長順 → 名前順
        """
        if len(self._files) <= 1:
            return

        # 最後に追加されたファイル群のフォルダを取得
        recent_folders = set()
        for file_data in self._files[-10:]:  # 直近10件をチェック
            recent_folders.add(file_data["folder"])

        if len(recent_folders) > 1:
            # 複数フォルダ: パス長順 → 名前順
            self._files.sort(key=lambda x: (len(x["folder"]), x["folder"], x["name"]))
        else:
            # 単一フォルダ: 名前順
            self._files.sort(key=lambda x: x["name"])

    def remove_files(self, indices: List[int]) -> None:
        """
        指定インデックスのファイルを削除

        Args:
            indices: 削除するインデックスのリスト
        """
        if not indices:
            return

        # 降順ソート（後ろから削除）
        indices_sorted = sorted(indices, reverse=True)
        removed_count = 0

        for idx in indices_sorted:
            if 0 <= idx < len(self._files):
                file_path = self._files[idx]["path"]
                self._file_paths_set.discard(file_path)
                del self._files[idx]
                removed_count += 1

        self.list_updated.emit(self._files)

        # ステータス通知
        if removed_count > 0:
            self.status_message.emit(
                self.tm.tr("notify.files_removed", count=removed_count)
            )

    def clear_all(self) -> None:
        """すべてのファイルを削除"""
        count = len(self._files)
        self._files.clear()
        self._file_paths_set.clear()
        self.list_updated.emit(self._files)

        # ステータス通知
        if count > 0:
            self.status_message.emit(self.tm.tr("notify.all_files_cleared"))

    def get_files_in_folder(self, folder_path: str) -> List[int]:
        """
        指定フォルダ内のファイルのインデックスを取得

        Args:
            folder_path: フォルダパス

        Returns:
            List[int]: インデックスのリスト
        """
        indices = []
        for i, file_data in enumerate(self._files):
            if file_data["folder"] == folder_path:
                indices.append(i)
        return indices

    def set_recursive(self, recursive: bool) -> None:
        """サブフォルダ再帰読み込みを設定"""
        self.recursive = recursive

    def update_file_status(self, file_path: str, status: str) -> None:
        """
        ファイルの処理ステータスを更新

        Args:
            file_path: ファイルパス
            status: "success" or "error"
        """
        for file_data in self._files:
            if file_data["path"] == file_path:
                file_data["status"] = status
                break

        # リスト更新を通知
        self.list_updated.emit(self._files)

    def reset_all_status(self) -> None:
        """すべてのファイルのステータスをpendingにリセット"""
        for file_data in self._files:
            file_data["status"] = STATUS_PENDING
        self.list_updated.emit(self._files)
