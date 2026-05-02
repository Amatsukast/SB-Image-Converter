"""
メインウィンドウ統合モジュール

レイアウト構築、画面切り替え、シグナル/スロット接続
"""

import subprocess
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLabel,
    QProgressBar,
    QStackedWidget,
    QFileDialog,
)
from PySide6.QtCore import Qt
from gui.toolbar import Toolbar
from gui.file_list import FileListWidget
from gui.settings_panel import SettingsPanel
from gui.settings_screen import SettingsScreen
from gui.dialogs import PauseDialog, CloseConfirmDialog
from core.file_manager import FileManager
from core.conversion_worker import ConversionWorker
from managers.settings_manager import SettingsManager
from managers.translation_manager import get_translation_manager


class MainWindow(QMainWindow):
    """メインウィンドウクラス"""

    # UI Constants
    DEFAULT_LEFT_WIDTH = 1050
    DEFAULT_RIGHT_WIDTH = 350

    def __init__(self) -> None:
        super().__init__()
        self.tm = get_translation_manager()
        self._setup_window()
        self._create_logic()
        self._create_widgets()
        self._setup_layout()
        self._connect_signals()
        self._load_settings()

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)

    def _setup_window(self) -> None:
        """ウィンドウ基本設定"""
        self.setWindowTitle("SB Image Converter")
        self.setMinimumSize(800, 600)
        self.resize(1400, 900)

    def _create_logic(self) -> None:
        """Logic層インスタンス作成"""
        self.settings_manager = SettingsManager()
        self.file_manager = FileManager(recursive=False)
        self.conversion_worker = ConversionWorker()

    def _create_widgets(self) -> None:
        """ウィジェット作成"""
        # 中央ウィジェット
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 画面切り替え用
        self.stacked_widget = QStackedWidget()

        # ツールバー
        self.toolbar = Toolbar()

        # プログレスエリア
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # テキスト非表示（高さが細いため）
        self.status_label = QLabel(self.tm.tr("status.ready"))
        self.status_label.setAlignment(Qt.AlignCenter)

        # メインエリア（2ペイン）
        self.splitter = QSplitter(Qt.Horizontal)

        # 左ペイン: ファイル一覧
        self.file_list_widget = FileListWidget()

        # 右ペイン: 設定パネル
        self.settings_panel = SettingsPanel()

        # スプリッターにウィジェット追加
        self.splitter.addWidget(self.file_list_widget)
        self.splitter.addWidget(self.settings_panel)
        # 右ペインを固定幅に
        self.splitter.setSizes([self.DEFAULT_LEFT_WIDTH, self.DEFAULT_RIGHT_WIDTH])
        self.splitter.setStretchFactor(0, 1)  # 左は伸縮
        self.splitter.setStretchFactor(1, 0)  # 右は固定幅維持

        # 下部エリア
        self.version_label = QLabel("v1.0.2")
        self.version_label.setAlignment(Qt.AlignLeft)
        self.version_label.setObjectName("versionLabel")
        self.version_label.setStyleSheet("font-size: 10px; padding: 5px;")

    def _setup_layout(self) -> None:
        """レイアウト構築"""
        # メイン画面レイアウト
        main_screen = QWidget()
        main_layout = QVBoxLayout(main_screen)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ツールバー追加
        main_layout.addWidget(self.toolbar)

        # プログレスエリア
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(16, 0, 16, 8)
        progress_layout.addWidget(self.status_label)
        progress_layout.addSpacing(6)
        progress_layout.addWidget(self.progress_bar)
        progress_widget = QWidget()
        progress_widget.setLayout(progress_layout)
        main_layout.addWidget(progress_widget)

        # メインエリア（スプリッター）
        main_layout.addWidget(self.splitter, 1)

        # 下部エリア
        main_layout.addWidget(self.version_label)

        # スタックウィジェットに追加
        self.stacked_widget.addWidget(main_screen)

        # 設定画面
        self.settings_screen = SettingsScreen()
        self.stacked_widget.addWidget(self.settings_screen)

        # 中央ウィジェットにレイアウト設定
        central_layout = QVBoxLayout(self.central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.stacked_widget)

    def _connect_signals(self) -> None:
        """シグナル/スロット接続"""
        # ツールバーシグナル接続
        self.toolbar.play_clicked.connect(self._on_play_clicked)
        self.toolbar.files_clicked.connect(self._on_select_files)
        self.toolbar.folder_clicked.connect(self._on_select_folder)
        self.toolbar.trash_clicked.connect(self._on_trash_clicked)
        self.toolbar.settings_clicked.connect(self._on_settings_clicked)
        self.toolbar.about_clicked.connect(self._on_about_clicked)

        # ファイル一覧 → ファイル管理
        self.file_list_widget.files_dropped.connect(self.file_manager.add_files)
        self.file_list_widget.remove_selected.connect(self.file_manager.remove_files)
        self.file_list_widget.remove_others.connect(self._on_remove_others)
        self.file_list_widget.open_folder.connect(self._on_open_folder)
        self.file_list_widget.load_same_folder.connect(self._on_load_same_folder)
        self.file_list_widget.add_files_requested.connect(self._on_select_files)
        self.file_list_widget.add_folder_requested.connect(self._on_select_folder)
        self.file_list_widget.clear_all_requested.connect(self._on_trash_clicked)

        # ファイル管理 → ファイル一覧
        self.file_manager.list_updated.connect(self.file_list_widget.update_display)
        self.file_manager.status_message.connect(self._on_status_message)

        # 設定パネル
        self.settings_panel.output_browse_clicked.connect(self._on_output_browse)

        # 変換ワーカー
        self.conversion_worker.progress_updated.connect(self._on_progress_updated)
        self.conversion_worker.conversion_started.connect(self._on_conversion_started)
        self.conversion_worker.conversion_completed.connect(
            self._on_conversion_completed
        )
        self.conversion_worker.file_processed.connect(self._on_file_processed)

        # 設定画面
        self.settings_screen.save_and_close_clicked.connect(self._on_settings_save)
        self.settings_screen.cancel_clicked.connect(self._on_settings_cancel)
        self.settings_screen.reset_defaults_clicked.connect(self._on_settings_reset)

    # === イベントハンドラ ===

    def _on_play_clicked(self) -> None:
        """再生/一時停止ボタンクリック"""
        # 実行中の場合は一時停止
        if self.conversion_worker.isRunning():
            self._on_pause()
            return

        # ファイルがない場合
        if self.file_manager.get_file_count() == 0:
            self.status_label.setText(self.tm.tr("status.no_files"))
            return

        # アイコンを一時停止に変更
        self.toolbar.set_playing_state(True)

        # ステータスをリセット（再実行時に備える）
        self.file_manager.reset_all_status()

        # 変換実行（バックグラウンドスレッド）
        file_list = self.file_manager.get_files()
        settings = self.settings_panel.get_settings()
        self.conversion_worker.set_task(file_list, settings)
        self.conversion_worker.start()

    def _on_select_folder(self) -> None:
        """フォルダ選択"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            self.tm.tr("dialog.select_folder"),
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if folder_path:
            self.file_manager.add_files([folder_path])

    def _on_select_files(self) -> None:
        """ファイル選択（複数可）"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            self.tm.tr("dialog.select_files"),
            "",
            self.tm.tr("dialog.file_filter"),
        )

        if file_paths:
            self.file_manager.add_files(file_paths)

    def _on_trash_clicked(self) -> None:
        """一掃ボタンクリック"""
        self.file_manager.clear_all()

    def _on_settings_clicked(self) -> None:
        """設定メニュークリック"""
        # 現在の右ペインの設定をsettings_managerに保存
        # （キャンセル時にmanagerから復元できるようにするため）
        current_panel_settings = self.settings_panel.get_settings()
        self.settings_manager.update(
            output_format=current_panel_settings.get("format", "WebP"),
            webp_quality=current_panel_settings.get("webp_quality", 90),
            webp_method=current_panel_settings.get("webp_method", 4),
            png_compress_level=current_panel_settings.get("png_compress", 4),
            png_optimize=current_panel_settings.get("png_optimize", False),
            jpg_quality=current_panel_settings.get("jpg_quality", 90),
            jpg_subsampling=current_panel_settings.get("jpg_subsample", "4:2:2"),
            jpg_progressive=current_panel_settings.get("jpg_progressive", False),
            resize_enabled=current_panel_settings.get("resize_enabled", False),
            resize_mode=current_panel_settings.get("resize_mode", "比率"),
            resize_percentage=current_panel_settings.get("resize_percent", 100),
            resize_px_width=current_panel_settings.get("resize_width", 1920),
            resize_px_height=current_panel_settings.get("resize_height", 1080),
            resize_edge_value=current_panel_settings.get("resize_long")
            or current_panel_settings.get("resize_short", 1920),
            output_path=current_panel_settings.get("output_path", "./converted/"),
        )
        # 設定画面に切り替え
        self.stacked_widget.setCurrentIndex(1)

    def _on_about_clicked(self) -> None:
        """バージョン情報クリック"""
        from gui.dialogs import AboutDialog

        dialog = AboutDialog(self)
        dialog.exec()

    def _on_settings_save(self) -> None:
        """設定画面: 保存して閉じる"""
        self._save_app_settings()
        self.stacked_widget.setCurrentIndex(0)

    def _on_settings_cancel(self) -> None:
        """設定画面: キャンセル"""
        # 設定画面と右ペインの両方をmanagerから復元（リセットも元に戻る）
        from dataclasses import asdict

        settings_dict = asdict(self.settings_manager.settings)
        self.settings_screen.load_settings(settings_dict)
        self.settings_panel.load_settings(settings_dict)
        self.stacked_widget.setCurrentIndex(0)

    def _on_settings_reset(self) -> None:
        """設定画面: デフォルトに戻す"""
        from gui.dialogs import ResetConfirmDialog

        dialog = ResetConfirmDialog(self)
        dialog.exec()

        if dialog.get_action() == "yes":
            from managers.settings_manager import AppSettings

            default_settings = AppSettings()
            from dataclasses import asdict

            settings_dict = asdict(default_settings)

            # 設定画面と右ペインの両方をリセット
            self.settings_screen.load_settings(settings_dict)
            self.settings_panel.load_settings(settings_dict)

    def _on_remove_others(self, selected_indices: list) -> None:
        """選択以外を削除"""
        all_indices = set(range(self.file_manager.get_file_count()))
        selected_set = set(selected_indices)
        remove_indices = sorted(all_indices - selected_set)
        self.file_manager.remove_files(remove_indices)

    def _on_open_folder(self, folder_path: str) -> None:
        """フォルダをエクスプローラーで開く"""
        folder = Path(folder_path)
        if folder.exists():
            if os.name == "nt":  # Windows
                os.startfile(folder)
            else:  # Mac/Linux
                subprocess.Popen(["xdg-open", folder])

    def _on_load_same_folder(self, folder_path: str) -> None:
        """同一フォルダの他の画像を読み込み"""
        self.file_manager.add_files([folder_path])

    def _on_output_browse(self) -> None:
        """出力先フォルダ参照ボタン"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            self.tm.tr("dialog.select_output_folder"),
            self.settings_panel.output_path.text() or "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if folder_path:
            self.settings_panel.output_path.setText(folder_path)

    def _on_status_message(self, message: str) -> None:
        """ステータスメッセージ更新"""
        self.status_label.setText(message)

    def _on_progress_updated(self, current: int, total: int) -> None:
        """進捗更新"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(
            self.tm.tr("status.processing", current=current, total=total)
        )

    def _on_conversion_started(self) -> None:
        """変換開始"""
        # ツールバーの再生ボタンを一時停止アイコンに
        self.toolbar.set_playing_state(True)

    def _on_conversion_completed(self, summary: dict) -> None:
        """変換完了"""
        # プログレスバーを最大値に設定（完了を視覚的に示す）
        self.progress_bar.setValue(self.progress_bar.maximum())

        # 停止された場合はキャンセル分を計算
        if summary.get("cancelled", 0) > 0:
            # 「停止」または「Stopped」だけに色をつける
            stopped_word = "停止" if self.tm.current_language == "ja" else "Stopped"
            colored_stopped = f"<span style='color:#ffa726'>{stopped_word}</span>"
            full_text = self.tm.tr(
                "status.stopped",
                success=summary["success"],
                cancelled=summary["cancelled"],
            )
            self.status_label.setText(full_text.replace(stopped_word, colored_stopped))
        else:
            success_count = summary["success"]
            error_count = summary["error"]

            # 完了ステータスを動的に変化
            if error_count == 0:
                # 全成功
                status_key = "status.completed"
                status_text = (
                    f"<span style='color:#4caf50'>{self.tm.tr(status_key)}</span>"
                )
            elif success_count == 0:
                # 全失敗
                status_key = "status.completed_all_failed"
                status_text = (
                    f"<span style='color:#f44336'>{self.tm.tr(status_key)}</span>"
                )
            else:
                # 一部エラー
                status_key = "status.completed_with_errors"
                status_text = (
                    f"<span style='color:#f44336'>{self.tm.tr(status_key)}</span>"
                )

            self.status_label.setText(
                self.tm.tr(
                    "status.completed_detail",
                    status=status_text,
                    success=success_count,
                    error=error_count,
                )
            )

        # ツールバーの再生ボタンを再生アイコンに戻す
        self.toolbar.set_playing_state(False)

    def _on_pause(self) -> None:
        """一時停止処理"""
        # 一時停止
        self.conversion_worker.pause()
        self.status_label.setText(self.tm.tr("status.paused"))

        # ダイアログ表示
        dialog = PauseDialog(self)
        dialog.exec()

        action = dialog.get_action()
        if action == "stop":
            # 停止（完了を待つ）
            self.conversion_worker.stop()
        elif action == "resume":
            # 再開
            self.conversion_worker.resume()

    def _on_file_processed(self, file_name: str, success: bool, message: str) -> None:
        """ファイル処理完了時"""
        # ファイル名からフルパスを取得してステータス更新
        for file_data in self.file_manager.get_files():
            if file_data["name"] == file_name:
                status = "success" if success else "error"
                self.file_manager.update_file_status(file_data["path"], status)
                break

    def _load_settings(self) -> None:
        """設定を読み込んでUIに反映"""
        from dataclasses import asdict

        settings_dict = asdict(self.settings_manager.settings)
        self.settings_panel.load_settings(settings_dict)
        self.settings_screen.load_settings(settings_dict)

        # ファイルマネージャーの設定
        self.file_manager.set_recursive(settings_dict.get("recursive_folder", False))

    def _save_settings(self) -> None:
        """現在のUI設定を保存"""
        current_settings = self.settings_panel.get_settings()

        # AppSettingsのフィールド名にマッピング
        self.settings_manager.update(
            output_format=current_settings.get("format", "WebP"),
            webp_quality=current_settings.get("webp_quality", 90),
            webp_method=current_settings.get("webp_method", 4),
            png_compress_level=current_settings.get("png_compress", 4),
            png_optimize=current_settings.get("png_optimize", False),
            jpg_quality=current_settings.get("jpg_quality", 90),
            jpg_subsampling=current_settings.get("jpg_subsample", "4:2:2"),
            jpg_progressive=current_settings.get("jpg_progressive", False),
            resize_enabled=current_settings.get("resize_enabled", False),
            resize_mode=current_settings.get("resize_mode", "パーセンテージ"),
            resize_percentage=current_settings.get("resize_percent", 100),
            resize_px_width=current_settings.get("resize_width", 1920),
            resize_px_height=current_settings.get("resize_height", 1080),
            resize_edge_value=current_settings.get("resize_long")
            or current_settings.get("resize_short", 1920),
            output_path=current_settings.get("output_path", "./converted/"),
        )

    def _save_app_settings(self) -> None:
        """Save settings screen configuration"""
        app_settings = self.settings_screen.get_settings()

        self.settings_manager.update(
            language=app_settings.get("language", "ja"),
            theme=app_settings.get("theme", "system"),
            recursive_folder=app_settings.get("recursive_folder", False),
            overwrite_mode=app_settings.get("overwrite_mode", False),
            keep_metadata=app_settings.get("keep_metadata", False),
            transparent_bg_color=app_settings.get("transparent_bg_color", "#FFFFFF"),
        )

        # Update file manager settings
        self.file_manager.set_recursive(app_settings.get("recursive_folder", False))

    def closeEvent(self, event):
        """ウィンドウ閉じる時の処理"""
        # 変換中の場合は確認
        if self.conversion_worker.isRunning():
            # 即座に一時停止
            self.conversion_worker.pause()

            # 終了確認ダイアログ表示
            dialog = CloseConfirmDialog(self)
            dialog.exec()

            action = dialog.get_action()
            if action == "exit":
                # 終了: 変換停止して終了
                self.conversion_worker.stop()
                self.conversion_worker.wait()
                self._save_settings()
                event.accept()
            else:
                # キャンセル（またはバツボタン）: 変換再開
                self.conversion_worker.resume()
                event.ignore()
        else:
            # 変換中でない場合は通常終了
            self._save_settings()
            event.accept()

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        # ステータスラベルのテキストを更新（変換中でなければ）
        if not self.conversion_worker.isRunning():
            self.status_label.setText(self.tm.tr("status.ready"))
