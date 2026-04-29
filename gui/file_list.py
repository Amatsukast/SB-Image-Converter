"""
ファイル一覧表示モジュール

QTreeView + Model、ドラッグ&ドロップ、コンテキストメニュー（View層）
"""

from pathlib import Path
from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QHeaderView,
    QMenu,
    QAbstractItemView,
    QLabel,
    QStyledItemDelegate,
)
from PySide6.QtCore import (
    Qt,
    Signal,
    QAbstractTableModel,
    QModelIndex,
    QMimeData,
    QUrl,
    QRect,
)
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QColor
from core.icon_loader import IconLoader
from managers.translation_manager import get_translation_manager
from managers.theme_manager import get_theme_manager


class FileListModel(QAbstractTableModel):
    """ファイルリスト用データモデル"""

    def __init__(self):
        super().__init__()
        self.tm = get_translation_manager()
        self._data: List[dict] = []

        # 言語切り替えに対応
        self.tm.language_changed.connect(self._on_language_changed)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 5  # ファイル名、解像度、サイズ、更新日時、フォルダパス

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return None

        file_data = self._data[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:  # ファイル名
                return file_data["name"]
            elif col == 1:  # 解像度
                return f"{file_data['width']}×{file_data['height']}"
            elif col == 2:  # サイズ
                return self._format_size(file_data["size"])
            elif col == 3:  # 更新日時
                return file_data["modified"].strftime("%Y-%m-%d %H:%M:%S")
            elif col == 4:  # フォルダパス
                return file_data["folder"]

        elif role == Qt.TextAlignmentRole:
            if col in (1, 2):  # 解像度、サイズは右寄せ
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.UserRole:
            # ステータス情報を返す（デリゲートで使用）
            return file_data.get("status", "pending")

        elif role == Qt.ToolTipRole:
            # フォルダパス列はツールチップでフルパス表示
            if col == 4:
                return file_data["folder"]

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole
    ):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            columns = [
                self.tm.tr("filelist.column.filename"),
                self.tm.tr("filelist.column.resolution"),
                self.tm.tr("filelist.column.size"),
                self.tm.tr("filelist.column.modified"),
                self.tm.tr("filelist.column.folder"),
            ]
            return columns[section]
        return None

    def update_data(self, file_list: List[dict]) -> None:
        """データ更新"""
        self.beginResetModel()
        self._data = file_list
        self.endResetModel()

    def get_file_data(self, row: int) -> Optional[dict]:
        """指定行のファイルデータを取得"""
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    @staticmethod
    def _format_size(size: int) -> str:
        """ファイルサイズをフォーマット"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def _on_language_changed(self) -> None:
        """言語切り替え時のヘッダー更新"""
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount() - 1)


class StatusBarDelegate(QStyledItemDelegate):
    """ステータスバー描画用カスタムデリゲート"""

    def paint(self, painter: QPainter, option, index: QModelIndex) -> None:
        # 通常の描画
        super().paint(painter, option, index)

        # 第0列（ファイル名列）のみバーを描画
        if index.column() != 0:
            return

        # ステータスを取得
        status = index.data(Qt.UserRole)

        # ステータスに応じて左端にバーを描画
        bar_width = 3
        bar_rect = QRect(
            option.rect.left(), option.rect.top(), bar_width, option.rect.height()
        )

        if status == "success":
            painter.fillRect(bar_rect, QColor("#4caf50"))  # 緑
        elif status == "error":
            painter.fillRect(bar_rect, QColor("#f44336"))  # 赤
        else:  # pending
            painter.fillRect(bar_rect, QColor("#4a4a4a"))  # グレー


class FileListWidget(QWidget):
    """ファイル一覧ウィジェット（View層）"""

    # UI Constants
    PLACEHOLDER_ICON_SIZE = 96

    # シグナル定義
    files_dropped = Signal(list)  # ファイル/フォルダがドロップされた
    remove_selected = Signal(list)  # 選択削除要求
    remove_others = Signal(list)  # 選択以外削除要求
    open_folder = Signal(str)  # フォルダを開く要求
    load_same_folder = Signal(str)  # 同一フォルダの画像読み込み要求
    add_files_requested = Signal()  # ファイル追加要求（空白右クリック用）
    add_folder_requested = Signal()  # フォルダ追加要求（空白右クリック用）
    clear_all_requested = Signal()  # 一掃要求（空白右クリック用）

    def __init__(self):
        super().__init__()
        self.tm = get_translation_manager()
        self.theme_manager = get_theme_manager()
        self._setup_ui()

        # 言語切り替えに対応
        self.tm.language_changed.connect(self.refresh_ui)
        # テーマ切り替えに対応
        self.theme_manager.theme_changed.connect(self._reload_placeholder_icon)

    def _setup_ui(self) -> None:
        """UI構築"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # テーブルビュー
        self.tree_view = QTreeView()
        self.model = FileListModel()
        self.tree_view.setModel(self.model)

        # カスタムデリゲートを設定（ステータスバー描画用）
        self.delegate = StatusBarDelegate()
        self.tree_view.setItemDelegate(self.delegate)

        # プレースホルダー（空状態表示）
        self.placeholder = QWidget(self.tree_view)
        self.placeholder.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )  # マウスイベントを透過
        self.placeholder.setStyleSheet(
            "QWidget { background: transparent; }"
        )  # 背景を透明に
        placeholder_layout = QVBoxLayout(self.placeholder)
        placeholder_layout.setSpacing(16)
        placeholder_layout.setContentsMargins(0, 0, 0, 0)

        # アイコン（placeholderTextと同じ色で生成）
        self.placeholder_icon_label = QLabel()
        placeholder_color = self.theme_manager.get_placeholder_color()
        icon = IconLoader.load(
            "file_open", size=self.PLACEHOLDER_ICON_SIZE, color=placeholder_color
        )
        self.placeholder_icon_label.setPixmap(icon.pixmap(96, 96))
        self.placeholder_icon_label.setAlignment(Qt.AlignCenter)

        # Placeholder text
        self.placeholder_text = QLabel(self.tm.tr("filelist.drop_hint"))
        self.placeholder_text.setAlignment(Qt.AlignCenter)
        self.placeholder_text.setObjectName("placeholderText")
        self.placeholder_text.setStyleSheet("""
            QLabel#placeholderText {
                font-size: 16px;
            }
        """)

        placeholder_layout.addWidget(self.placeholder_icon_label)
        placeholder_layout.addWidget(self.placeholder_text)

        self._update_placeholder_visibility()

        # ツリービュー設定
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_view.setAlternatingRowColors(False)  # 交互の色を無効化
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setRootIsDecorated(False)  # 階層表示アイコンを非表示
        self.tree_view.setItemsExpandable(False)  # 展開機能を無効化
        self.tree_view.setUniformRowHeights(True)  # パフォーマンス向上
        self.tree_view.setFocusPolicy(Qt.NoFocus)  # フォーカスフレームを無効化
        self.tree_view.setTextElideMode(Qt.ElideMiddle)  # 中央省略

        # 列幅調整
        header = self.tree_view.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # ファイル名: 伸縮
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 解像度
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # サイズ
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 更新日時
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # フォルダパス: 伸縮

        # ドラッグ&ドロップ設定（ファイルドロップのみ受け付け）
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDragEnabled(False)
        self.tree_view.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)

        # コンテキストメニュー
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._show_context_menu)

        layout.addWidget(self.tree_view)

    def update_display(self, file_list: List[dict]) -> None:
        """ファイルリスト表示を更新"""
        self.model.update_data(file_list)
        self._update_placeholder_visibility()

    def get_selected_indices(self) -> List[int]:
        """選択されている行のインデックスを取得"""
        selected_rows = set()
        for index in self.tree_view.selectedIndexes():
            selected_rows.add(index.row())
        return sorted(selected_rows)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ドラッグ開始"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """ドロップ受付"""
        mime_data: QMimeData = event.mimeData()

        if mime_data.hasUrls():
            paths = []
            for url in mime_data.urls():
                if url.isLocalFile():
                    paths.append(url.toLocalFile())

            if paths:
                self.files_dropped.emit(paths)
                event.acceptProposedAction()

    def _show_context_menu(self, position) -> None:
        """コンテキストメニュー表示"""
        selected_indices = self.get_selected_indices()
        has_files = self.model.rowCount() > 0

        menu = QMenu(self)

        if not selected_indices:
            # 空白部分を右クリック
            # ファイル/フォルダ追加
            add_files_action = menu.addAction(self.tm.tr("filelist.context.add_files"))
            add_files_action.setIcon(IconLoader.load("image"))
            add_files_action.triggered.connect(self.add_files_requested.emit)

            add_folder_action = menu.addAction(
                self.tm.tr("filelist.context.add_folder")
            )
            add_folder_action.setIcon(IconLoader.load("folder"))
            add_folder_action.triggered.connect(self.add_folder_requested.emit)

            menu.addSeparator()

            # 全て削除（常に表示、ファイルがない時は無効化）
            clear_action = menu.addAction(self.tm.tr("filelist.context.clear_all"))
            clear_action.setIcon(IconLoader.load("delete"))
            clear_action.setEnabled(has_files)
            clear_action.triggered.connect(self.clear_all_requested.emit)

        else:
            # ファイルを選択している場合
            # 選択を一覧から削除
            remove_action = menu.addAction(
                self.tm.tr("filelist.context.remove_selected")
            )
            remove_action.triggered.connect(
                lambda: self.remove_selected.emit(selected_indices)
            )

            menu.addSeparator()

            # ファイルの場所を開く
            if len(selected_indices) == 1:
                file_data = self.model.get_file_data(selected_indices[0])
                if file_data:
                    folder_path = file_data["folder"]

                    open_folder_action = menu.addAction(
                        self.tm.tr("filelist.context.open_folder")
                    )
                    open_folder_action.triggered.connect(
                        lambda: self.open_folder.emit(folder_path)
                    )

                    # 同一フォルダの他の画像を全部読み込み
                    load_same_action = menu.addAction(
                        self.tm.tr("filelist.context.load_same_folder")
                    )
                    load_same_action.triggered.connect(
                        lambda: self.load_same_folder.emit(folder_path)
                    )

                    menu.addSeparator()

            # 選択以外を削除
            if selected_indices:
                remove_others_action = menu.addAction(
                    self.tm.tr("filelist.context.remove_others")
                )
                remove_others_action.triggered.connect(
                    lambda: self.remove_others.emit(selected_indices)
                )

        # メニュー表示
        menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def resizeEvent(self, event):
        """リサイズ時にプレースホルダーの位置を調整"""
        super().resizeEvent(event)
        self._update_placeholder_geometry()

    def showEvent(self, event):
        """表示時にプレースホルダーの位置を調整"""
        super().showEvent(event)
        self._update_placeholder_geometry()

    def _update_placeholder_visibility(self) -> None:
        """プレースホルダーの表示/非表示を切り替え"""
        has_files = self.model.rowCount() > 0
        self.placeholder.setVisible(not has_files)
        if not has_files:
            self._update_placeholder_geometry()

    def _update_placeholder_geometry(self) -> None:
        """プレースホルダーの位置とサイズを調整"""
        # TreeViewのビューポートの中央に配置
        viewport_rect = self.tree_view.viewport().rect()
        placeholder_width = 400
        placeholder_height = 140

        # ヘッダー分のオフセットを考慮
        header_height = self.tree_view.header().height()
        x = (viewport_rect.width() - placeholder_width) // 2
        y = header_height + (viewport_rect.height() - placeholder_height) // 2

        self.placeholder.setGeometry(x, y, placeholder_width, placeholder_height)

    def _reload_placeholder_icon(self) -> None:
        """テーマ切り替え時にプレースホルダーアイコンを再読み込み"""
        placeholder_color = self.theme_manager.get_placeholder_color()
        icon = IconLoader.load(
            "file_open", size=self.PLACEHOLDER_ICON_SIZE, color=placeholder_color
        )
        self.placeholder_icon_label.setPixmap(icon.pixmap(96, 96))

    def refresh_ui(self) -> None:
        """言語切り替え時のUI更新"""
        # プレースホルダーのテキストを更新
        self.placeholder_text.setText(self.tm.tr("filelist.drop_hint"))
