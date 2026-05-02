"""
カスタムウィジェット

再利用可能なカスタムウィジェットの定義
"""

from PySide6.QtWidgets import QComboBox, QSlider


class NoScrollComboBox(QComboBox):
    """マウスホイールスクロールを無効化したQComboBox

    通常のQComboBoxではマウスホイールで項目が変わってしまうが、
    このクラスではスクロールイベントを無視して意図しない変更を防ぐ。
    """

    def wheelEvent(self, event):
        """マウスホイールイベントを無視"""
        event.ignore()


class NoScrollSlider(QSlider):
    """マウスホイールスクロールを無効化したQSlider

    通常のQSliderではマウスホイールで値が変わってしまうが、
    このクラスではスクロールイベントを無視して意図しない変更を防ぐ。
    """

    def wheelEvent(self, event):
        """マウスホイールイベントを無視"""
        event.ignore()
