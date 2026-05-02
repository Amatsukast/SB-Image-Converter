"""
ダイアログモジュール

一時停止ダイアログ、確認ダイアログ等
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices, QCursor
from managers.translation_manager import get_translation_manager


class PauseDialog(QDialog):
    """一時停止ダイアログ"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tm = get_translation_manager()
        self._setup_ui()
        self.result_action = None  # "stop" or "resume"

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)

    def _setup_ui(self) -> None:
        """UI構築"""
        self.setWindowTitle(self.tm.tr("dialog.pause.title"))
        self.setModal(True)
        self.setFixedSize(350, 150)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # メッセージ
        self.message = QLabel(self.tm.tr("dialog.pause.message"))
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.message)

        # ボタン
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.resume_button = QPushButton(self.tm.tr("dialog.resume"))
        self.resume_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.resume_button.clicked.connect(self._on_resume)

        self.stop_button = QPushButton(self.tm.tr("dialog.stop"))
        self.stop_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.stop_button.clicked.connect(self._on_stop)

        button_layout.addWidget(self.resume_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

    def _on_stop(self) -> None:
        """停止ボタン"""
        self.result_action = "stop"
        self.accept()

    def _on_resume(self) -> None:
        """再開ボタン"""
        self.result_action = "resume"
        self.accept()

    def get_action(self) -> str:
        """選択されたアクションを取得"""
        return self.result_action

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        self.setWindowTitle(self.tm.tr("dialog.pause.title"))
        self.message.setText(self.tm.tr("dialog.pause.message"))
        self.resume_button.setText(self.tm.tr("dialog.resume"))
        self.stop_button.setText(self.tm.tr("dialog.stop"))


class CloseConfirmDialog(QDialog):
    """終了確認ダイアログ（変換処理中）"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tm = get_translation_manager()
        self._setup_ui()
        self.result_action = None  # "exit" or "cancel"

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)

    def _setup_ui(self) -> None:
        """UI構築"""
        self.setWindowTitle(self.tm.tr("dialog.close.title"))
        self.setModal(True)
        self.setFixedSize(400, 150)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # メッセージ
        self.message = QLabel(self.tm.tr("dialog.close.message"))
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.message)

        # ボタン
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton(self.tm.tr("dialog.cancel"))
        self.cancel_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.cancel_button.clicked.connect(self._on_cancel)

        self.exit_button = QPushButton(self.tm.tr("dialog.exit"))
        self.exit_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.exit_button.clicked.connect(self._on_exit)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.exit_button)

        layout.addLayout(button_layout)

    def _on_exit(self) -> None:
        """終了ボタン"""
        self.result_action = "exit"
        self.accept()

    def _on_cancel(self) -> None:
        """キャンセルボタン"""
        self.result_action = "cancel"
        self.reject()

    def get_action(self) -> str:
        """選択されたアクションを取得"""
        return self.result_action

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        self.setWindowTitle(self.tm.tr("dialog.close.title"))
        self.message.setText(self.tm.tr("dialog.close.message"))
        self.cancel_button.setText(self.tm.tr("dialog.cancel"))
        self.exit_button.setText(self.tm.tr("dialog.exit"))


class ResetConfirmDialog(QDialog):
    """設定リセット確認ダイアログ"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tm = get_translation_manager()
        self._setup_ui()
        self.result_action = None  # "yes" or "no"

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)

    def _setup_ui(self) -> None:
        """UI構築"""
        self.setWindowTitle(self.tm.tr("dialog.reset.title"))
        self.setModal(True)
        self.setFixedSize(450, 180)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # メッセージ
        self.message = QLabel(self.tm.tr("dialog.reset.message"))
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.message)

        # ボタン
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.no_button = QPushButton(self.tm.tr("dialog.no"))
        self.no_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.no_button.clicked.connect(self._on_no)

        self.yes_button = QPushButton(self.tm.tr("dialog.yes"))
        self.yes_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.yes_button.clicked.connect(self._on_yes)

        button_layout.addWidget(self.no_button)
        button_layout.addWidget(self.yes_button)

        layout.addLayout(button_layout)

    def _on_yes(self) -> None:
        """はいボタン"""
        self.result_action = "yes"
        self.accept()

    def _on_no(self) -> None:
        """いいえボタン"""
        self.result_action = "no"
        self.reject()

    def get_action(self) -> str:
        """選択されたアクションを取得"""
        return self.result_action

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        self.setWindowTitle(self.tm.tr("dialog.reset.title"))
        self.message.setText(self.tm.tr("dialog.reset.message"))
        self.no_button.setText(self.tm.tr("dialog.no"))
        self.yes_button.setText(self.tm.tr("dialog.yes"))


class AboutDialog(QDialog):
    """バージョン情報ダイアログ"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tm = get_translation_manager()
        self._setup_ui()

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)

    def _setup_ui(self) -> None:
        """UI構築"""
        self.setWindowTitle(self.tm.tr("dialog.about.title"))
        self.setModal(True)
        self.setFixedSize(500, 320)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # アプリ名
        app_name = QLabel("SB Image Converter")
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(app_name)

        # バージョン
        self.version_label = QLabel(self.tm.tr("dialog.about.version"))
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(self.version_label)

        layout.addSpacing(10)

        # 説明
        self.description = QLabel(self.tm.tr("dialog.about.description"))
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("font-size: 13px;")
        self.description.setWordWrap(True)
        layout.addWidget(self.description)

        layout.addSpacing(10)

        # GitHubリンク
        github_link = QLabel(
            '<a href="https://github.com/Amatsukast/SB-Image-Converter" style="color: #0066cc;">GitHub Repository</a>'
        )
        github_link.setAlignment(Qt.AlignCenter)
        github_link.setOpenExternalLinks(True)
        github_link.setStyleSheet("font-size: 13px;")
        github_link.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(github_link)

        # ライセンス
        self.license_label = QLabel(self.tm.tr("dialog.about.license"))
        self.license_label.setAlignment(Qt.AlignCenter)
        self.license_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.license_label)

        layout.addSpacing(5)

        # 著者
        self.author_label = QLabel(self.tm.tr("dialog.about.author"))
        self.author_label.setAlignment(Qt.AlignCenter)
        self.author_label.setStyleSheet("font-size: 12px; color: #666;")
        layout.addWidget(self.author_label)

        layout.addStretch()

        # 閉じるボタン
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.close_button = QPushButton(self.tm.tr("dialog.about.close"))
        self.close_button.setStyleSheet("padding: 12px 18px; font-size: 16px;")
        self.close_button.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        self.setWindowTitle(self.tm.tr("dialog.about.title"))
        self.version_label.setText(self.tm.tr("dialog.about.version"))
        self.description.setText(self.tm.tr("dialog.about.description"))
        self.license_label.setText(self.tm.tr("dialog.about.license"))
        self.author_label.setText(self.tm.tr("dialog.about.author"))
        self.close_button.setText(self.tm.tr("dialog.about.close"))
