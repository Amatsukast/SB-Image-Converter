"""
設定画面モジュール

テーマ設定、詳細オプション設定（View層）
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QRadioButton,
    QButtonGroup,
    QPushButton,
    QGroupBox,
    QScrollArea,
    QColorDialog,
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QColor
from core.icon_loader import IconLoader
from managers.translation_manager import get_translation_manager
from managers.theme_manager import get_theme_manager
from config.constants import LANG_SYSTEM, LANG_JAPANESE, LANG_ENGLISH


def _create_section_title(text: str) -> QLabel:
    """セクションタイトル作成"""
    label = QLabel(text)
    label.setObjectName("sectionTitle")
    label.setStyleSheet("""
        QLabel#sectionTitle {
            font-size: 20px;
            font-weight: bold;
        }
    """)
    return label


def _create_separator() -> QWidget:
    """区切り線作成"""
    line = QWidget()
    line.setFixedHeight(1)
    line.setStyleSheet("background-color: #3a3a3a;")
    return line


def _create_note_label(text: str) -> QLabel:
    """注釈ラベル作成"""
    label = QLabel(text)
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    label.setObjectName("noteLabel")
    label.setStyleSheet("""
        QLabel#noteLabel {
            font-size: 12px;
        }
    """)
    return label


class SettingsScreen(QWidget):
    """設定画面クラス（View層）"""

    # シグナル定義
    save_and_close_clicked = Signal()  # 保存して閉じる
    cancel_clicked = Signal()  # キャンセル
    reset_defaults_clicked = Signal()  # デフォルトに戻す

    def __init__(self) -> None:
        super().__init__()
        self.tm = get_translation_manager()
        self.theme_manager = get_theme_manager()
        self._setup_ui()
        self.tm.language_changed.connect(self.refresh_ui)
        self.theme_manager.theme_changed.connect(self._reload_icons)

    def _setup_ui(self) -> None:
        """UI構築"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # メインコンテナ
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 24, 32, 16)
        layout.setSpacing(0)

        # タイトル
        self.title_label = QLabel(self.tm.tr("settings_screen.title"))
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(self.title_label)
        layout.addSpacing(20)

        # ボタンエリア
        layout.addWidget(self._create_button_area())
        layout.addSpacing(24)

        # 外観設定（言語 + テーマ）
        self.appearance_section_title = _create_section_title(
            self.tm.tr("settings_screen.appearance")
        )
        layout.addWidget(self.appearance_section_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_appearance_section())
        layout.addSpacing(24)

        # 区切り線
        layout.addWidget(_create_separator())
        layout.addSpacing(24)

        # 動作設定
        self.behavior_section_title = _create_section_title(
            self.tm.tr("settings_screen.behavior")
        )
        layout.addWidget(self.behavior_section_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_behavior_section())
        layout.addSpacing(24)

        # 区切り線
        layout.addWidget(_create_separator())
        layout.addSpacing(24)

        # 画像処理設定
        self.image_section_title = _create_section_title(
            self.tm.tr("settings_screen.image_processing")
        )
        layout.addWidget(self.image_section_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_image_section())

        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_appearance_section(self) -> QWidget:
        """外観設定セクション（言語 + テーマ）"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 言語選択
        self.language_label = QLabel(self.tm.tr("settings_screen.language"))
        self.language_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.language_label)
        layout.addSpacing(6)
        self.language_combo = QComboBox()
        self.language_combo.addItem(
            self.tm.tr("settings_screen.language.system"), LANG_SYSTEM
        )
        self.language_combo.addItem(
            self.tm.tr("settings_screen.language.english"), LANG_ENGLISH
        )
        self.language_combo.addItem(
            self.tm.tr("settings_screen.language.japanese"), LANG_JAPANESE
        )
        self.language_combo.setFixedWidth(318)
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        layout.addWidget(self.language_combo)

        layout.addSpacing(24)

        # テーマ選択
        self.theme_label = QLabel(self.tm.tr("settings_screen.theme.label"))
        self.theme_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.theme_label)
        layout.addSpacing(6)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(self.tm.tr("settings_screen.theme.system"), "system")
        self.theme_combo.addItem(self.tm.tr("settings_screen.theme.light"), "light")
        self.theme_combo.addItem(self.tm.tr("settings_screen.theme.dark"), "dark")
        self.theme_combo.setFixedWidth(318)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        layout.addWidget(self.theme_combo)

        return widget

    def _on_language_changed(self, index: int) -> None:
        """言語変更時の処理"""
        language_code = self.language_combo.itemData(index)
        if language_code:
            self.tm.set_language(language_code)

    def _on_theme_changed(self, index: int) -> None:
        """テーマ変更時の処理"""
        theme_code = self.theme_combo.itemData(index)
        if theme_code:
            theme_manager = get_theme_manager()
            theme_manager.set_theme(theme_code)

    def _create_behavior_section(self) -> QWidget:
        """動作設定セクション"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # サブフォルダ再帰読み込み
        self.recursive_checkbox = QCheckBox(
            self.tm.tr("settings_screen.behavior.recursive")
        )
        layout.addWidget(self.recursive_checkbox)
        layout.addSpacing(24)

        # 同名ファイルの処理
        overwrite_section = QVBoxLayout()
        overwrite_section.setSpacing(8)
        self.overwrite_label = QLabel(
            self.tm.tr("settings_screen.behavior.overwrite_label")
        )
        self.overwrite_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        overwrite_section.addWidget(self.overwrite_label)

        self.overwrite_group = QButtonGroup(self)
        self.overwrite_rename = QRadioButton(
            self.tm.tr("settings_screen.behavior.overwrite_rename")
        )
        self.overwrite_yes = QRadioButton(
            self.tm.tr("settings_screen.behavior.overwrite_yes")
        )

        self.overwrite_group.addButton(self.overwrite_rename, 0)
        self.overwrite_group.addButton(self.overwrite_yes, 1)
        self.overwrite_rename.setChecked(True)

        overwrite_section.addWidget(self.overwrite_rename)
        overwrite_section.addWidget(self.overwrite_yes)
        layout.addLayout(overwrite_section)

        return widget

    def _create_image_section(self) -> QWidget:
        """画像処理設定セクション"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # メタデータ保持
        self.keep_metadata_checkbox = QCheckBox(
            self.tm.tr("settings_screen.image_processing.keep_metadata")
        )
        layout.addWidget(self.keep_metadata_checkbox)
        layout.addSpacing(24)

        # 透過背景色
        bg_section = QVBoxLayout()
        bg_section.setSpacing(8)
        self.bg_label = QLabel(
            self.tm.tr("settings_screen.image_processing.bg_color_label")
        )
        self.bg_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        bg_section.addWidget(self.bg_label)

        bg_layout = QHBoxLayout()
        self.bg_color_button = QPushButton()
        self.bg_color_button.setFixedSize(60, 30)
        self.bg_color_button.clicked.connect(self._on_bg_color_clicked)
        self._current_bg_color = "#FFFFFF"
        self._update_bg_color_button()

        bg_layout.addWidget(self.bg_color_button)
        bg_layout.addStretch()
        bg_section.addLayout(bg_layout)
        layout.addLayout(bg_section)

        return widget

    def _on_bg_color_clicked(self) -> None:
        """背景色選択ボタンクリック"""
        current_color = QColor(self._current_bg_color)
        color = QColorDialog.getColor(
            current_color,
            self,
            self.tm.tr("settings_screen.image_processing.bg_color_dialog"),
        )

        if color.isValid():
            self._current_bg_color = color.name()
            self._update_bg_color_button()

    def _update_bg_color_button(self) -> None:
        """背景色ボタンの表示更新"""
        self.bg_color_button.setStyleSheet(
            f"background-color: {self._current_bg_color}; border: 1px solid #666;"
        )

    def get_settings(self) -> dict:
        """Get settings values"""
        return {
            "language": self.language_combo.currentData(),
            "theme": self.theme_combo.currentData(),
            "recursive_folder": self.recursive_checkbox.isChecked(),
            "overwrite_mode": self.overwrite_yes.isChecked(),
            "keep_metadata": self.keep_metadata_checkbox.isChecked(),
            "transparent_bg_color": self._current_bg_color,
        }

    def load_settings(self, settings: dict) -> None:
        """Load settings values to UI"""
        # Language
        language = settings.get("language", "ja")
        lang_index = self.language_combo.findData(language)
        if lang_index >= 0:
            self.language_combo.setCurrentIndex(lang_index)

        # Theme
        theme = settings.get("theme", "system")
        theme_index = self.theme_combo.findData(theme)
        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(theme_index)

        # Recursive folder
        self.recursive_checkbox.setChecked(settings.get("recursive_folder", False))

        # 上書きモード
        if settings.get("overwrite_mode", False):
            self.overwrite_yes.setChecked(True)
        else:
            self.overwrite_rename.setChecked(True)

        # メタデータ保持
        self.keep_metadata_checkbox.setChecked(settings.get("keep_metadata", False))

        # 背景色
        self._current_bg_color = settings.get("transparent_bg_color", "#FFFFFF")
        self._update_bg_color_button()

    def _reload_icons(self) -> None:
        """テーマ切り替え時にアイコンを再読み込み"""
        self.reset_button.setIcon(IconLoader.load("reset_settings", size=32))
        self.cancel_button.setIcon(IconLoader.load("close", size=32))
        self.save_button.setIcon(IconLoader.load("save", size=32))

    def refresh_ui(self) -> None:
        """言語変更時にUI全体のテキストを更新"""
        # タイトル
        self.title_label.setText(self.tm.tr("settings_screen.title"))

        # セクションタイトル
        self.appearance_section_title.setText(self.tm.tr("settings_screen.appearance"))
        self.behavior_section_title.setText(self.tm.tr("settings_screen.behavior"))
        self.image_section_title.setText(self.tm.tr("settings_screen.image_processing"))

        # 外観セクション - 言語
        self.language_label.setText(self.tm.tr("settings_screen.language"))
        current_language_index = self.language_combo.currentIndex()
        self.language_combo.blockSignals(True)
        self.language_combo.setItemText(
            0, self.tm.tr("settings_screen.language.system")
        )
        self.language_combo.setItemText(
            1, self.tm.tr("settings_screen.language.english")
        )
        self.language_combo.setItemText(
            2, self.tm.tr("settings_screen.language.japanese")
        )
        self.language_combo.blockSignals(False)

        # 外観セクション - テーマ
        self.theme_label.setText(self.tm.tr("settings_screen.theme.label"))
        current_theme_data = self.theme_combo.currentData()
        self.theme_combo.setItemText(0, self.tm.tr("settings_screen.theme.system"))
        self.theme_combo.setItemText(1, self.tm.tr("settings_screen.theme.light"))
        self.theme_combo.setItemText(2, self.tm.tr("settings_screen.theme.dark"))
        index = self.theme_combo.findData(current_theme_data)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        # 動作セクション
        self.recursive_checkbox.setText(
            self.tm.tr("settings_screen.behavior.recursive")
        )
        self.overwrite_label.setText(
            self.tm.tr("settings_screen.behavior.overwrite_label")
        )
        self.overwrite_rename.setText(
            self.tm.tr("settings_screen.behavior.overwrite_rename")
        )
        self.overwrite_yes.setText(self.tm.tr("settings_screen.behavior.overwrite_yes"))

        # 画像処理セクション
        self.keep_metadata_checkbox.setText(
            self.tm.tr("settings_screen.image_processing.keep_metadata")
        )
        self.bg_label.setText(
            self.tm.tr("settings_screen.image_processing.bg_color_label")
        )

        # ボタンエリア
        self.reset_button.setText(self.tm.tr("settings_screen.button.reset"))
        self.cancel_button.setText(self.tm.tr("settings_screen.button.cancel"))
        self.save_button.setText(self.tm.tr("settings_screen.button.save"))

    def _create_button_area(self) -> QWidget:
        """ボタンエリア作成"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 10)

        # デフォルトに戻すボタン（左寄せ）
        self.reset_button = QPushButton(self.tm.tr("settings_screen.button.reset"))
        self.reset_button.setIcon(IconLoader.load("reset_settings", size=32))
        self.reset_button.setIconSize(QSize(32, 32))
        self.reset_button.setStyleSheet("padding: 14px 20px; font-size: 18px;")
        self.reset_button.clicked.connect(self.reset_defaults_clicked.emit)
        layout.addWidget(self.reset_button)

        layout.addStretch()

        # キャンセルボタン
        self.cancel_button = QPushButton(self.tm.tr("settings_screen.button.cancel"))
        self.cancel_button.setIcon(IconLoader.load("close", size=32))
        self.cancel_button.setIconSize(QSize(32, 32))
        self.cancel_button.setStyleSheet("padding: 14px 20px; font-size: 18px;")
        self.cancel_button.clicked.connect(self.cancel_clicked.emit)
        layout.addWidget(self.cancel_button)

        # 保存して閉じるボタン
        self.save_button = QPushButton(self.tm.tr("settings_screen.button.save"))
        self.save_button.setIcon(IconLoader.load("save", size=32))
        self.save_button.setIconSize(QSize(32, 32))
        self.save_button.setStyleSheet("padding: 14px 20px; font-size: 18px;")
        self.save_button.clicked.connect(self.save_and_close_clicked.emit)
        layout.addWidget(self.save_button)

        return widget
