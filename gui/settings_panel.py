"""
設定パネルモジュール

出力フォーマット選択、リサイズ設定、品質設定（View層）
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QStackedWidget,
    QScrollArea,
    QFrame,
    QSlider,
)
from PySide6.QtCore import Qt, Signal, QSize
from core.icon_loader import IconLoader
from managers.translation_manager import get_translation_manager
from managers.theme_manager import get_theme_manager
from config.constants import (
    RESIZE_MODE_RATIO,
    RESIZE_MODE_PIXELS,
    RESIZE_MODE_LONG_EDGE,
    RESIZE_MODE_SHORT_EDGE,
)


class SettingsPanel(QWidget):
    """設定パネルクラス（View層）"""

    # シグナル定義
    settings_changed = Signal(dict)  # 設定変更時
    output_browse_clicked = Signal()  # 参照ボタンクリック

    def __init__(self) -> None:
        super().__init__()
        self.tm = get_translation_manager()
        self.theme_manager = get_theme_manager()
        self._setup_ui()

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)
        # テーマ切り替えに対応
        self.theme_manager.theme_changed.connect(self._reload_icons)

    def _setup_ui(self) -> None:
        """UI構築"""
        # スクロールエリア
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # メインコンテナ
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        # 出力フォーマット
        self.format_title = self._create_section_title(
            self.tm.tr("settings.section.output_format")
        )
        layout.addWidget(self.format_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_format_section())
        layout.addSpacing(24)

        # 区切り線
        layout.addWidget(self._create_separator())
        layout.addSpacing(24)

        # リサイズ設定
        self.resize_title = self._create_section_title(
            self.tm.tr("settings.section.resize")
        )
        layout.addWidget(self.resize_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_resize_section())
        layout.addSpacing(24)

        # 区切り線
        layout.addWidget(self._create_separator())
        layout.addSpacing(24)

        # 出力先設定
        self.output_title = self._create_section_title(
            self.tm.tr("settings.section.output_path")
        )
        layout.addWidget(self.output_title)
        layout.addSpacing(10)
        layout.addWidget(self._create_output_section())

        layout.addStretch()

        scroll.setWidget(container)

        # レイアウト設定
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_section_title(self, text: str) -> QLabel:
        """セクションタイトル作成"""
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        label.setStyleSheet("""
            QLabel#sectionTitle {
                font-size: 16px;
                font-weight: bold;
            }
        """)
        return label

    def _create_separator(self) -> QWidget:
        """区切り線作成"""
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #3a3a3a;")
        return line

    def _create_quality_slider(
        self,
        min_val: int,
        max_val: int,
        default_val: int,
        label_text: str,
        note_text: str,
    ) -> tuple:
        """
        Create quality slider with spinbox (reusable pattern)

        Returns:
            tuple: (spinbox, slider, label, note_label, header_layout)
        """
        # Header with label and spinbox
        header = QHBoxLayout()
        label = QLabel(label_text)
        header.addWidget(label)
        header.addStretch()

        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        spinbox.setButtonSymbols(QSpinBox.NoButtons)
        spinbox.setFixedWidth(70)
        spinbox.setAlignment(Qt.AlignRight)
        header.addWidget(spinbox)

        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)

        # Connect spinbox and slider
        spinbox.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(spinbox.setValue)

        # Note label
        note_label = self._create_note_label(note_text)

        return spinbox, slider, label, note_label, header

    def _create_note_label(self, text: str) -> QLabel:
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

    def _create_format_section(self) -> QWidget:
        """出力フォーマットセクション"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # フォーマット選択
        self.format_combo = QComboBox()
        self.format_combo.addItems(["WebP", "PNG", "JPG", "BMP"])
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        layout.addWidget(self.format_combo)

        layout.addSpacing(24)

        # フォーマット別詳細設定
        self.format_stack = QStackedWidget()
        self.format_stack.addWidget(self._create_webp_widget())
        self.format_stack.addWidget(self._create_png_widget())
        self.format_stack.addWidget(self._create_jpg_widget())
        self.format_stack.addWidget(self._create_bmp_widget())
        layout.addWidget(self.format_stack)

        return widget

    def _create_webp_widget(self) -> QWidget:
        """WebP設定ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Quality slider
        (
            self.webp_quality,
            self.webp_quality_slider,
            self.webp_quality_label,
            self.webp_quality_note,
            quality_header,
        ) = self._create_quality_slider(
            0,
            100,
            90,
            self.tm.tr("settings.webp.quality"),
            self.tm.tr("settings.webp.quality_note"),
        )
        layout.addLayout(quality_header)
        layout.addWidget(self.webp_quality_slider)
        layout.addWidget(self.webp_quality_note)

        layout.addSpacing(8)

        # 圧縮メソッド（ラベル + 数値）
        method_header = QHBoxLayout()
        self.webp_method_label = QLabel(self.tm.tr("settings.webp.method"))
        method_header.addWidget(self.webp_method_label)
        method_header.addStretch()
        self.webp_method = QSpinBox()
        self.webp_method.setRange(0, 6)
        self.webp_method.setValue(4)
        self.webp_method.setButtonSymbols(QSpinBox.NoButtons)
        self.webp_method.setFixedWidth(70)
        self.webp_method.setAlignment(Qt.AlignRight)
        method_header.addWidget(self.webp_method)
        layout.addLayout(method_header)

        # スライダー
        self.webp_method_slider = QSlider(Qt.Horizontal)
        self.webp_method_slider.setRange(0, 6)
        self.webp_method_slider.setValue(4)
        layout.addWidget(self.webp_method_slider)

        # 連動
        self.webp_method.valueChanged.connect(self.webp_method_slider.setValue)
        self.webp_method_slider.valueChanged.connect(self.webp_method.setValue)

        # 注釈
        self.webp_method_note = self._create_note_label(
            self.tm.tr("settings.webp.method_note")
        )
        layout.addWidget(self.webp_method_note)

        return widget

    def _create_png_widget(self) -> QWidget:
        """PNG設定ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Compress level slider
        (
            self.png_compress,
            self.png_compress_slider,
            self.png_compress_label,
            self.png_compress_note,
            compress_header,
        ) = self._create_quality_slider(
            0,
            9,
            4,
            self.tm.tr("settings.png.compress_level"),
            self.tm.tr("settings.png.compress_level_note"),
        )
        layout.addLayout(compress_header)
        layout.addWidget(self.png_compress_slider)
        layout.addWidget(self.png_compress_note)

        layout.addSpacing(8)

        # 最適化
        self.png_optimize_label = QLabel(self.tm.tr("settings.png.optimize"))
        self.png_optimize_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.png_optimize_label)
        self.png_optimize = QCheckBox(self.tm.tr("settings.png.optimize_enable"))
        layout.addWidget(self.png_optimize)
        self.png_optimize_note = self._create_note_label(
            self.tm.tr("settings.png.optimize_note")
        )
        layout.addWidget(self.png_optimize_note)

        return widget

    def _create_jpg_widget(self) -> QWidget:
        """JPG設定ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Quality slider
        (
            self.jpg_quality,
            self.jpg_quality_slider,
            self.jpg_quality_label,
            self.jpg_quality_note,
            quality_header,
        ) = self._create_quality_slider(
            0,
            100,
            90,
            self.tm.tr("settings.jpg.quality"),
            self.tm.tr("settings.jpg.quality_note"),
        )
        layout.addLayout(quality_header)
        layout.addWidget(self.jpg_quality_slider)
        layout.addWidget(self.jpg_quality_note)

        layout.addSpacing(8)

        # サブサンプリングとプログレッシブを横並び
        options_layout = QHBoxLayout()

        # サブサンプリング
        subsample_section = QVBoxLayout()
        subsample_section.setSpacing(6)
        subsample_section.setAlignment(Qt.AlignTop)
        self.jpg_subsample_label = QLabel(self.tm.tr("settings.jpg.subsampling"))
        self.jpg_subsample_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        subsample_section.addWidget(self.jpg_subsample_label)
        self.jpg_subsample = QComboBox()
        self.jpg_subsample.addItems(["4:4:4", "4:2:2", "4:2:0"])
        self.jpg_subsample.setCurrentText("4:2:2")
        subsample_section.addWidget(self.jpg_subsample)
        options_layout.addLayout(subsample_section)

        options_layout.addSpacing(20)

        # プログレッシブ
        progressive_section = QVBoxLayout()
        progressive_section.setSpacing(6)
        progressive_section.setAlignment(Qt.AlignTop)
        self.jpg_progressive_label = QLabel(self.tm.tr("settings.jpg.progressive"))
        self.jpg_progressive_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        progressive_section.addWidget(self.jpg_progressive_label)
        self.jpg_progressive = QCheckBox(self.tm.tr("settings.jpg.progressive_enable"))
        progressive_section.addWidget(self.jpg_progressive)
        options_layout.addLayout(progressive_section)

        options_layout.addStretch()
        layout.addLayout(options_layout)

        return widget

    def _create_bmp_widget(self) -> QWidget:
        """BMP設定ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.bmp_note = self._create_note_label(self.tm.tr("settings.bmp.no_options"))
        layout.addWidget(self.bmp_note)
        return widget

    def _create_resize_section(self) -> QWidget:
        """リサイズセクション"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # リサイズ有効化
        self.resize_enabled = QCheckBox(self.tm.tr("settings.resize.enable"))
        layout.addWidget(self.resize_enabled)

        layout.addSpacing(16)

        # リサイズ詳細
        self.resize_detail_widget = QWidget()
        detail_layout = QVBoxLayout(self.resize_detail_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(0)

        # モード選択
        self.resize_mode_label = QLabel(self.tm.tr("settings.resize.mode"))
        self.resize_mode_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        detail_layout.addWidget(self.resize_mode_label)
        detail_layout.addSpacing(6)
        self.resize_mode = QComboBox()
        # リサイズモードの表示名を翻訳キー経由で設定
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_RATIO), RESIZE_MODE_RATIO
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_PIXELS), RESIZE_MODE_PIXELS
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_LONG_EDGE),
            RESIZE_MODE_LONG_EDGE,
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_SHORT_EDGE),
            RESIZE_MODE_SHORT_EDGE,
        )
        self.resize_mode.currentIndexChanged.connect(self._on_resize_mode_changed)
        detail_layout.addWidget(self.resize_mode)

        detail_layout.addSpacing(16)

        # 値入力（モードに応じて変化）
        self.resize_value_stack = QStackedWidget()
        self.resize_value_stack.addWidget(self._create_percent_widget())
        self.resize_value_stack.addWidget(self._create_px_widget())
        self.resize_value_stack.addWidget(self._create_long_widget())
        self.resize_value_stack.addWidget(self._create_short_widget())
        detail_layout.addWidget(self.resize_value_stack)

        layout.addWidget(self.resize_detail_widget)

        return widget

    def _create_percent_widget(self) -> QWidget:
        """パーセンテージ入力ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # 倍率
        self.resize_percent_label = QLabel(self.tm.tr("settings.resize.percentage"))
        self.resize_percent_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.resize_percent_label)
        layout.addSpacing(6)
        percent_layout = QHBoxLayout()
        percent_layout.setSpacing(8)
        self.resize_percent = QSpinBox()
        self.resize_percent.setRange(1, 500)
        self.resize_percent.setValue(100)
        self.resize_percent.setButtonSymbols(QSpinBox.NoButtons)
        self.resize_percent.setAlignment(Qt.AlignRight)
        self.resize_percent.setFixedWidth(120)
        percent_layout.addWidget(self.resize_percent)
        self.resize_percent_unit = QLabel(self.tm.tr("settings.resize.percentage_unit"))
        percent_layout.addWidget(self.resize_percent_unit)
        layout.addLayout(percent_layout)

        return widget

    def _create_px_widget(self) -> QWidget:
        """px指定入力ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # 幅と高さを横並び
        size_layout = QHBoxLayout()

        # 幅
        width_section = QVBoxLayout()
        width_section.setSpacing(6)
        self.resize_width_label = QLabel(self.tm.tr("settings.resize.width"))
        self.resize_width_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        width_section.addWidget(self.resize_width_label)
        width_input = QHBoxLayout()
        width_input.setSpacing(8)
        self.resize_width = QSpinBox()
        self.resize_width.setRange(1, 50000)
        self.resize_width.setValue(1920)
        self.resize_width.setButtonSymbols(QSpinBox.NoButtons)
        self.resize_width.setAlignment(Qt.AlignRight)
        self.resize_width.setFixedWidth(120)
        width_input.addWidget(self.resize_width)
        self.resize_width_unit = QLabel(self.tm.tr("settings.resize.px_unit"))
        width_input.addWidget(self.resize_width_unit)
        width_section.addLayout(width_input)
        size_layout.addLayout(width_section)

        size_layout.addSpacing(20)

        # 高さ
        height_section = QVBoxLayout()
        height_section.setSpacing(6)
        self.resize_height_label = QLabel(self.tm.tr("settings.resize.height"))
        self.resize_height_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        height_section.addWidget(self.resize_height_label)
        height_input = QHBoxLayout()
        height_input.setSpacing(8)
        self.resize_height = QSpinBox()
        self.resize_height.setRange(1, 50000)
        self.resize_height.setValue(1080)
        self.resize_height.setButtonSymbols(QSpinBox.NoButtons)
        self.resize_height.setAlignment(Qt.AlignRight)
        self.resize_height.setFixedWidth(120)
        height_input.addWidget(self.resize_height)
        self.resize_height_unit = QLabel(self.tm.tr("settings.resize.px_unit"))
        height_input.addWidget(self.resize_height_unit)
        height_section.addLayout(height_input)
        size_layout.addLayout(height_section)

        layout.addLayout(size_layout)

        return widget

    def _create_long_widget(self) -> QWidget:
        """長辺基準入力ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        self.resize_long_label = QLabel(self.tm.tr("settings.resize.edge_value"))
        self.resize_long_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.resize_long_label)
        layout.addSpacing(6)
        value_layout = QHBoxLayout()
        value_layout.setSpacing(8)
        self.resize_long = QSpinBox()
        self.resize_long.setRange(1, 50000)
        self.resize_long.setValue(1920)
        self.resize_long.setButtonSymbols(QSpinBox.NoButtons)
        self.resize_long.setAlignment(Qt.AlignRight)
        self.resize_long.setFixedWidth(120)
        value_layout.addWidget(self.resize_long)
        self.resize_long_unit = QLabel(self.tm.tr("settings.resize.px_unit"))
        value_layout.addWidget(self.resize_long_unit)
        layout.addLayout(value_layout)
        return widget

    def _create_short_widget(self) -> QWidget:
        """短辺基準入力ウィジェット"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        self.resize_short_label = QLabel(self.tm.tr("settings.resize.edge_value"))
        self.resize_short_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.resize_short_label)
        layout.addSpacing(6)
        value_layout = QHBoxLayout()
        value_layout.setSpacing(8)
        self.resize_short = QSpinBox()
        self.resize_short.setRange(1, 50000)
        self.resize_short.setValue(1080)
        self.resize_short.setButtonSymbols(QSpinBox.NoButtons)
        self.resize_short.setAlignment(Qt.AlignRight)
        self.resize_short.setFixedWidth(120)
        value_layout.addWidget(self.resize_short)
        self.resize_short_unit = QLabel(self.tm.tr("settings.resize.px_unit"))
        value_layout.addWidget(self.resize_short_unit)
        layout.addLayout(value_layout)
        return widget

    def _create_output_section(self) -> QWidget:
        """出力先セクション"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # 出力先パス
        path_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("./converted/")
        self.output_path.setClearButtonEnabled(True)  # クリアボタン有効化
        path_layout.addWidget(self.output_path)

        # 参照ボタン（小さめアイコンボタン）
        self.output_browse = QPushButton()
        folder_icon = IconLoader.load("folder", size=22)
        self.output_browse.setIcon(folder_icon)
        self.output_browse.setIconSize(QSize(22, 22))
        self.output_browse.setFixedSize(36, 36)
        self.output_browse.clicked.connect(self.output_browse_clicked.emit)
        path_layout.addWidget(self.output_browse)
        layout.addLayout(path_layout)

        # 注釈
        self.output_note = self._create_note_label(
            self.tm.tr("settings.output.default_note")
        )
        layout.addWidget(self.output_note)

        return widget

    def _on_format_changed(self, format_name: str) -> None:
        """フォーマット変更時"""
        index = self.format_combo.currentIndex()
        self.format_stack.setCurrentIndex(index)

    def _on_resize_mode_changed(self, index: int) -> None:
        """リサイズモード変更"""
        self.resize_value_stack.setCurrentIndex(index)

    def get_settings(self) -> dict:
        """設定値を取得"""
        # 出力パス: 空欄の場合はデフォルト値を使用
        output_path = self.output_path.text()
        if not output_path:
            output_path = "./converted/"

        settings = {
            "format": self.format_combo.currentText(),
            "resize_enabled": self.resize_enabled.isChecked(),
            "output_path": output_path,
        }

        # フォーマット別設定
        format_name = settings["format"]
        if format_name == "WebP":
            settings["webp_quality"] = self.webp_quality.value()
            settings["webp_method"] = self.webp_method.value()
        elif format_name == "PNG":
            settings["png_compress"] = self.png_compress.value()
            settings["png_optimize"] = self.png_optimize.isChecked()
        elif format_name == "JPG":
            settings["jpg_quality"] = self.jpg_quality.value()
            settings["jpg_subsample"] = self.jpg_subsample.currentText()
            settings["jpg_progressive"] = self.jpg_progressive.isChecked()

        # リサイズ設定
        if settings["resize_enabled"]:
            # コンボボックスのユーザーデータから内部定数を取得
            mode_constant = self.resize_mode.currentData()
            settings["resize_mode"] = mode_constant
            if mode_constant == RESIZE_MODE_RATIO:
                settings["resize_percent"] = self.resize_percent.value()
            elif mode_constant == RESIZE_MODE_PIXELS:
                settings["resize_width"] = self.resize_width.value()
                settings["resize_height"] = self.resize_height.value()
            elif mode_constant == RESIZE_MODE_LONG_EDGE:
                settings["resize_long"] = self.resize_long.value()
            elif mode_constant == RESIZE_MODE_SHORT_EDGE:
                settings["resize_short"] = self.resize_short.value()

        return settings

    def load_settings(self, settings: dict) -> None:
        """設定値をUIに反映"""
        # 出力フォーマット（"format" または "output_format" キーに対応）
        format_name = settings.get("format") or settings.get("output_format", "WebP")
        self.format_combo.setCurrentText(format_name)

        # WebP
        self.webp_quality.setValue(settings.get("webp_quality", 90))
        self.webp_method.setValue(settings.get("webp_method", 4))

        # PNG
        self.png_compress.setValue(settings.get("png_compress_level", 4))
        self.png_optimize.setChecked(settings.get("png_optimize", False))

        # JPG
        self.jpg_quality.setValue(settings.get("jpg_quality", 90))
        self.jpg_subsample.setCurrentText(settings.get("jpg_subsampling", "4:2:2"))
        self.jpg_progressive.setChecked(settings.get("jpg_progressive", False))

        # リサイズ
        self.resize_enabled.setChecked(settings.get("resize_enabled", False))
        mode = settings.get("resize_mode", RESIZE_MODE_RATIO)
        # 内部定数から表示名に変換してコンボボックスを設定
        for i in range(self.resize_mode.count()):
            if self.resize_mode.itemData(i) == mode:
                self.resize_mode.setCurrentIndex(i)
                break
        self.resize_percent.setValue(settings.get("resize_percentage", 100))
        self.resize_width.setValue(settings.get("resize_px_width", 1920))
        self.resize_height.setValue(settings.get("resize_px_height", 1080))

        edge_value = settings.get("resize_edge_value", 1920)
        self.resize_long.setValue(edge_value)
        self.resize_short.setValue(edge_value)

        # 出力先（デフォルト空欄、カスタムパスのみ復元）
        saved_path = settings.get("output_path", "")
        if saved_path and saved_path != "./converted/":
            self.output_path.setText(saved_path)
        else:
            self.output_path.clear()

    def _reload_icons(self) -> None:
        """テーマ切り替え時にアイコンを再読み込み"""
        self.output_browse.setIcon(IconLoader.load("folder", size=22))

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        # セクションタイトル
        self.format_title.setText(self.tm.tr("settings.section.output_format"))
        self.resize_title.setText(self.tm.tr("settings.section.resize"))
        self.output_title.setText(self.tm.tr("settings.section.output_path"))

        # WebP
        self.webp_quality_label.setText(self.tm.tr("settings.webp.quality"))
        self.webp_quality_note.setText(self.tm.tr("settings.webp.quality_note"))
        self.webp_method_label.setText(self.tm.tr("settings.webp.method"))
        self.webp_method_note.setText(self.tm.tr("settings.webp.method_note"))

        # PNG
        self.png_compress_label.setText(self.tm.tr("settings.png.compress_level"))
        self.png_compress_note.setText(self.tm.tr("settings.png.compress_level_note"))
        self.png_optimize_label.setText(self.tm.tr("settings.png.optimize"))
        self.png_optimize.setText(self.tm.tr("settings.png.optimize_enable"))
        self.png_optimize_note.setText(self.tm.tr("settings.png.optimize_note"))

        # JPG
        self.jpg_quality_label.setText(self.tm.tr("settings.jpg.quality"))
        self.jpg_quality_note.setText(self.tm.tr("settings.jpg.quality_note"))
        self.jpg_subsample_label.setText(self.tm.tr("settings.jpg.subsampling"))
        self.jpg_progressive_label.setText(self.tm.tr("settings.jpg.progressive"))
        self.jpg_progressive.setText(self.tm.tr("settings.jpg.progressive_enable"))

        # BMP
        self.bmp_note.setText(self.tm.tr("settings.bmp.no_options"))

        # リサイズ
        self.resize_enabled.setText(self.tm.tr("settings.resize.enable"))
        self.resize_mode_label.setText(self.tm.tr("settings.resize.mode"))

        # リサイズモードコンボボックスの項目を更新
        current_mode = self.resize_mode.currentData()
        self.resize_mode.blockSignals(True)
        self.resize_mode.clear()
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_RATIO), RESIZE_MODE_RATIO
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_PIXELS), RESIZE_MODE_PIXELS
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_LONG_EDGE),
            RESIZE_MODE_LONG_EDGE,
        )
        self.resize_mode.addItem(
            self.tm.get_resize_mode_display(RESIZE_MODE_SHORT_EDGE),
            RESIZE_MODE_SHORT_EDGE,
        )
        # 選択を復元
        for i in range(self.resize_mode.count()):
            if self.resize_mode.itemData(i) == current_mode:
                self.resize_mode.setCurrentIndex(i)
                break
        self.resize_mode.blockSignals(False)

        # リサイズ値のラベル
        self.resize_percent_label.setText(self.tm.tr("settings.resize.percentage"))
        self.resize_percent_unit.setText(self.tm.tr("settings.resize.percentage_unit"))
        self.resize_width_label.setText(self.tm.tr("settings.resize.width"))
        self.resize_width_unit.setText(self.tm.tr("settings.resize.px_unit"))
        self.resize_height_label.setText(self.tm.tr("settings.resize.height"))
        self.resize_height_unit.setText(self.tm.tr("settings.resize.px_unit"))
        self.resize_long_label.setText(self.tm.tr("settings.resize.edge_value"))
        self.resize_long_unit.setText(self.tm.tr("settings.resize.px_unit"))
        self.resize_short_label.setText(self.tm.tr("settings.resize.edge_value"))
        self.resize_short_unit.setText(self.tm.tr("settings.resize.px_unit"))

        # 出力先
        self.output_note.setText(self.tm.tr("settings.output.default_note"))
