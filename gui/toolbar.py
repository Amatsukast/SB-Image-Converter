"""
ツールバーモジュール

ボタン配置、メニュー管理、シグナル発行
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMenu
from PySide6.QtCore import Signal, QSize, Qt, QPoint
from core.icon_loader import IconLoader
from managers.translation_manager import get_translation_manager
from managers.theme_manager import get_theme_manager


class Toolbar(QWidget):
    """ツールバークラス"""

    # UI Constants
    TOOLBAR_ICON_SIZE = 48
    TOOLBAR_BUTTON_SIZE = 72

    # シグナル定義
    settings_clicked = Signal()  # 設定メニュー
    about_clicked = Signal()  # バージョン情報
    files_clicked = Signal()  # ファイル選択
    folder_clicked = Signal()  # フォルダ選択
    trash_clicked = Signal()
    play_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.tm = get_translation_manager()
        self.theme_manager = get_theme_manager()
        self._is_playing = False
        self._drag_start_position = None  # ドラッグ開始位置
        self._drag_offset = None  # ウィンドウとマウスのオフセット
        self._setup_ui()
        self._create_menu()  # メニューを最初に作成して再利用

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)
        # テーマ切り替えに対応
        self.theme_manager.theme_changed.connect(self._reload_icons)

    def _setup_ui(self) -> None:
        """UI構築"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 4)
        layout.setSpacing(0)

        # 左カラム：ボタン群
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        self.menu_button = self._create_button("menu", self.tm.tr("toolbar.menu"))
        self.menu_button.clicked.connect(self._show_menu)

        self.files_button = self._create_button(
            "image", self.tm.tr("toolbar.add_files")
        )
        self.files_button.clicked.connect(self.files_clicked.emit)

        self.folder_button = self._create_button(
            "folder", self.tm.tr("toolbar.add_folder")
        )
        self.folder_button.clicked.connect(self.folder_clicked.emit)

        self.trash_button = self._create_button(
            "delete", self.tm.tr("toolbar.clear_all")
        )
        self.trash_button.clicked.connect(self.trash_clicked.emit)

        left_layout.addWidget(self.menu_button)
        left_layout.addWidget(self.files_button)
        left_layout.addWidget(self.folder_button)
        left_layout.addWidget(self.trash_button)
        left_layout.addStretch()

        # 中央カラム：再生ボタン
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        self.play_button = self._create_play_button(
            "play_circle", self.tm.tr("toolbar.start")
        )
        self.play_button.clicked.connect(self._on_play_button_clicked)
        center_layout.addWidget(self.play_button)

        # 右カラム：空（左と同じ幅を確保）
        right_widget = QWidget()

        # メインレイアウトに追加（1:0:1の比率で左右を同じ幅に）
        layout.addWidget(left_widget, 1)
        layout.addWidget(center_widget, 0)
        layout.addWidget(right_widget, 1)

    def _create_button(self, icon_name: str, tooltip: str) -> QPushButton:
        """ボタン作成ヘルパー"""
        button = QPushButton()
        button.setIcon(IconLoader.load(icon_name, size=self.TOOLBAR_ICON_SIZE))
        button.setIconSize(QSize(self.TOOLBAR_ICON_SIZE, self.TOOLBAR_ICON_SIZE))
        button.setToolTip(tooltip)
        button.setFixedSize(self.TOOLBAR_BUTTON_SIZE, self.TOOLBAR_BUTTON_SIZE)
        button.setObjectName(f"{icon_name}Button")
        return button

    def _create_play_button(self, icon_name: str, tooltip: str) -> QPushButton:
        """再生ボタン作成ヘルパー（_create_buttonと同じ）"""
        return self._create_button(icon_name, tooltip)

    def _on_play_button_clicked(self) -> None:
        """再生/一時停止ボタンクリック"""
        # アイコン切り替えはmain_window側で制御
        self.play_clicked.emit()

    def set_playing_state(self, is_playing: bool) -> None:
        """再生状態を外部から設定"""
        if self._is_playing != is_playing:
            self._is_playing = is_playing
            if is_playing:
                self.play_button.setIcon(
                    IconLoader.load("pause_circle", size=self.TOOLBAR_ICON_SIZE)
                )
                self.play_button.setToolTip(self.tm.tr("toolbar.pause"))
            else:
                self.play_button.setIcon(
                    IconLoader.load("play_circle", size=self.TOOLBAR_ICON_SIZE)
                )
                self.play_button.setToolTip(self.tm.tr("toolbar.start"))

    def _create_menu(self) -> None:
        """メニューを作成（初回のみ、再利用）"""
        self.menu = QMenu(self)

        # 設定
        self.settings_action = self.menu.addAction(self.tm.tr("toolbar.settings"))
        self.settings_action.setIcon(IconLoader.load("settings"))
        self.settings_action.triggered.connect(self.settings_clicked.emit)

        self.menu.addSeparator()

        # バージョン情報
        self.about_action = self.menu.addAction(self.tm.tr("toolbar.about"))
        self.about_action.setIcon(IconLoader.load("info"))
        self.about_action.triggered.connect(self.about_clicked.emit)

    def _show_menu(self) -> None:
        """メニュー表示"""
        # ボタンの下に表示
        button_pos = self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())
        self.menu.popup(button_pos)

    def _reload_icons(self) -> None:
        """テーマ切り替え時にアイコンを再読み込み"""
        self.menu_button.setIcon(IconLoader.load("menu", size=self.TOOLBAR_ICON_SIZE))
        self.files_button.setIcon(IconLoader.load("image", size=self.TOOLBAR_ICON_SIZE))
        self.folder_button.setIcon(
            IconLoader.load("folder", size=self.TOOLBAR_ICON_SIZE)
        )
        self.trash_button.setIcon(
            IconLoader.load("delete", size=self.TOOLBAR_ICON_SIZE)
        )

        # 再生ボタンは現在の状態に応じて
        if self._is_playing:
            self.play_button.setIcon(
                IconLoader.load("pause_circle", size=self.TOOLBAR_ICON_SIZE)
            )
        else:
            self.play_button.setIcon(
                IconLoader.load("play_circle", size=self.TOOLBAR_ICON_SIZE)
            )

        # メニューアイコンも再読み込み
        self.settings_action.setIcon(IconLoader.load("settings"))
        self.about_action.setIcon(IconLoader.load("info"))

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        # ボタンのツールチップを更新
        self.menu_button.setToolTip(self.tm.tr("toolbar.menu"))
        self.files_button.setToolTip(self.tm.tr("toolbar.add_files"))
        self.folder_button.setToolTip(self.tm.tr("toolbar.add_folder"))
        self.trash_button.setToolTip(self.tm.tr("toolbar.clear_all"))

        # 再生ボタンのツールチップを現在の状態に合わせて更新
        if self._is_playing:
            self.play_button.setToolTip(self.tm.tr("toolbar.pause"))
        else:
            self.play_button.setToolTip(self.tm.tr("toolbar.start"))

        # メニューアクションのテキストを更新
        self.settings_action.setText(self.tm.tr("toolbar.settings"))
        self.about_action.setText(self.tm.tr("toolbar.about"))

    def mousePressEvent(self, event):
        """マウス押下時 - ドラッグ開始位置を記録"""
        if event.button() == Qt.LeftButton:
            # クリック位置にウィジェット（ボタン等）があるか確認
            child_widget = self.childAt(event.pos())
            # 空白部分（ボタン以外）ならドラッグ開始位置を記録
            if child_widget is None or not isinstance(child_widget, QPushButton):
                self._drag_start_position = event.pos()
                self._drag_offset = None  # まだドラッグ開始していない
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """マウス移動時 - 5px以上動いたらウィンドウを移動"""
        if self._drag_start_position is not None:
            # 5px以上移動したかチェック
            distance = (event.pos() - self._drag_start_position).manhattanLength()
            if distance >= 5:
                # 最大化状態では何もしない
                if self.window().isMaximized():
                    return

                # 初回のみオフセットを計算
                if self._drag_offset is None:
                    self._drag_offset = (
                        event.globalPosition().toPoint()
                        - self.window().frameGeometry().topLeft()
                    )

                # ウィンドウを移動
                self.window().move(event.globalPosition().toPoint() - self._drag_offset)
                event.accept()
                return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """マウスを離した時 - ドラッグ状態をリセット"""
        if event.button() == Qt.LeftButton:
            self._drag_start_position = None
            self._drag_offset = None
        super().mouseReleaseEvent(event)
