"""
Translation dictionary

This is the ONLY file that contains Japanese text in the entire codebase.
All UI-facing text is managed here for easy maintenance and localization.
"""

from config.constants import (
    RESIZE_MODE_RATIO,
    RESIZE_MODE_PIXELS,
    RESIZE_MODE_LONG_EDGE,
    RESIZE_MODE_SHORT_EDGE,
    LANG_JAPANESE,
    LANG_ENGLISH,
)

TRANSLATIONS = {
    LANG_JAPANESE: {
        # ========================================
        # Toolbar
        # ========================================
        "toolbar.menu": "メニュー",
        "toolbar.add_files": "ファイルを追加",
        "toolbar.add_folder": "フォルダを追加",
        "toolbar.clear_all": "すべて削除",
        "toolbar.start": "変換開始",
        "toolbar.pause": "一時停止",
        "toolbar.resume": "再開",
        "toolbar.stop": "停止",
        "toolbar.settings": "設定",
        "toolbar.about": "バージョン情報",
        # ========================================
        # File List
        # ========================================
        "filelist.column.filename": "ファイル名",
        "filelist.column.resolution": "解像度",
        "filelist.column.size": "サイズ",
        "filelist.column.modified": "更新日時",
        "filelist.column.folder": "フォルダパス",
        "filelist.drop_hint": "ファイルをドラッグ&ドロップ",
        "filelist.context.add_files": "ファイルを追加",
        "filelist.context.add_folder": "フォルダを追加",
        "filelist.context.remove_selected": "選択を一覧から削除",
        "filelist.context.remove_others": "選択以外を削除",
        "filelist.context.clear_all": "全てを一覧から削除",
        "filelist.context.open_folder": "ファイルの場所を開く",
        "filelist.context.load_same_folder": "同一フォルダの他の画像を全部読み込み",
        # ========================================
        # Settings Panel - Sections
        # ========================================
        "settings.section.output_format": "出力フォーマット",
        "settings.section.resize": "リサイズ",
        "settings.section.output_path": "出力先",
        # ========================================
        # Settings Panel - Format Options
        # ========================================
        "settings.format.webp": "WebP",
        "settings.format.png": "PNG",
        "settings.format.jpg": "JPG",
        "settings.format.bmp": "BMP",
        # ========================================
        # Settings Panel - WebP Options
        # ========================================
        "settings.webp.quality": "品質",
        "settings.webp.quality_note": "品質100で自動的にロスレス",
        "settings.webp.method": "圧縮メソッド",
        "settings.webp.method_note": "0=高速（大きめ）、6=低速（小さめ）",
        # ========================================
        # Settings Panel - PNG Options
        # ========================================
        "settings.png.compress_level": "圧縮レベル",
        "settings.png.compress_level_note": "0=無圧縮（高速）、9=最大圧縮（低速）",
        "settings.png.optimize": "最適化",
        "settings.png.optimize_enable": "有効",
        "settings.png.optimize_note": "ファイルサイズ削減、処理時間増加",
        # ========================================
        # Settings Panel - JPG Options
        # ========================================
        "settings.jpg.quality": "品質",
        "settings.jpg.quality_note": "0=最低品質、100=最高品質",
        "settings.jpg.subsampling": "サブサンプリング",
        "settings.jpg.progressive": "プログレッシブ",
        "settings.jpg.progressive_enable": "有効",
        "settings.jpg.transparent_bg": "透明部分の背景色",
        # ========================================
        # Settings Panel - BMP Options
        # ========================================
        "settings.bmp.no_options": "設定項目なし",
        # ========================================
        # Settings Panel - Resize Options
        # ========================================
        "settings.resize.enable": "リサイズを有効にする",
        "settings.resize.mode": "モード",
        "settings.resize.mode.ratio": "比率",
        "settings.resize.mode.pixels": "px指定",
        "settings.resize.mode.long_edge": "長辺基準",
        "settings.resize.mode.short_edge": "短辺基準",
        "settings.resize.percentage": "パーセンテージ",
        "settings.resize.percentage_unit": "%",
        "settings.resize.width": "幅",
        "settings.resize.height": "高さ",
        "settings.resize.edge_value": "辺の長さ",
        "settings.resize.px_unit": "px",
        # ========================================
        # Settings Panel - Output Path
        # ========================================
        "settings.output.path": "出力先パス",
        "settings.output.browse": "参照",
        "settings.output.default_note": "デフォルト: 元フォルダ内に ./converted/ 作成",
        "settings.output.relative_note": "相対パス（元画像と同じ階層に出力）",
        "settings.output.numbering": "連番サフィックス",
        "settings.output.numbering_enable": "有効",
        "settings.output.numbering_note": "同名ファイルが存在する場合に _001, _002... を付与",
        "settings.output.keep_metadata": "メタデータを保持",
        "settings.output.keep_metadata_enable": "有効",
        # ========================================
        # Settings Screen
        # ========================================
        "settings_screen.title": "設定",
        "settings_screen.appearance": "外観",
        "settings_screen.language": "言語",
        "settings_screen.language.system": "システム設定",
        "settings_screen.language.english": "English",
        "settings_screen.language.japanese": "日本語",
        "settings_screen.theme": "テーマ",
        "settings_screen.theme.label": "テーマ",
        "settings_screen.theme.system": "システム設定",
        "settings_screen.theme.dark": "ダークモード",
        "settings_screen.theme.light": "ライトモード",
        "settings_screen.behavior": "動作",
        "settings_screen.behavior.recursive": "サブフォルダを読み込む",
        "settings_screen.behavior.overwrite_label": "同名ファイルが存在する場合",
        "settings_screen.behavior.overwrite_rename": "連番サフィックスで別名保存（推奨）",
        "settings_screen.behavior.overwrite_yes": "上書きする",
        "settings_screen.image_processing": "画像処理",
        "settings_screen.image_processing.keep_metadata": "メタデータ（Exif等）を保持する",
        "settings_screen.image_processing.bg_color_label": "透過画像のJPG変換時の背景色",
        "settings_screen.image_processing.bg_color_dialog": "背景色を選択",
        "settings_screen.button.reset": " デフォルトに戻す",
        "settings_screen.button.cancel": " キャンセル",
        "settings_screen.button.save": " 保存して閉じる",
        "settings_screen.close": "閉じる",
        "settings_screen.save": "保存",
        # ========================================
        # Dialogs
        # ========================================
        "dialog.confirm": "確認",
        "dialog.error": "エラー",
        "dialog.info": "情報",
        "dialog.yes": "はい",
        "dialog.no": "いいえ",
        "dialog.ok": "OK",
        "dialog.cancel": "キャンセル",
        "dialog.resume": "再開",
        "dialog.stop": "停止",
        "dialog.exit": "終了",
        "dialog.pause.title": "一時停止",
        "dialog.pause.message": "変換処理を一時停止しました",
        "dialog.close.title": "確認",
        "dialog.close.message": "変換処理が実行中です。\nこのまま終了しますか？",
        "dialog.reset.title": "確認",
        "dialog.reset.message": "すべての設定を初期値に戻しますか？\n（出力フォーマット、リサイズ、品質設定なども含む）",
        "dialog.select_folder": "フォルダを選択",
        "dialog.select_files": "画像ファイルを選択（複数選択可）",
        "dialog.select_output_folder": "出力先フォルダを選択",
        "dialog.file_filter": "画像ファイル (*.webp *.png *.jpg *.jpeg *.bmp);;すべてのファイル (*.*)",
        "dialog.clear_all.message": "すべてのファイルを削除しますか？",
        "dialog.output_folder.title": "出力先フォルダを選択",
        "dialog.about.title": "バージョン情報",
        "dialog.about.version": "Version 1.0.3",
        "dialog.about.description": "シンプルで効率的なバッチ画像変換ツール",
        "dialog.about.license": "License: GNU General Public License v3.0",
        "dialog.about.author": "© 2026 Amatsukast",
        "dialog.about.close": "閉じる",
        # ========================================
        # Status Messages
        # ========================================
        "status.ready": "待機中",
        "status.no_files": "処理する画像がありません",
        "status.processing": "処理中: {current} / {total}",
        "status.stopped": "停止: 完了 {success}件 / キャンセル {cancelled}件",
        "status.completed": "完了",
        "status.completed_all_failed": "完了（全て失敗）",
        "status.completed_with_errors": "完了（エラーあり）",
        "status.completed_detail": "{status} : 成功 {success}件 / 失敗 {error}件",
        "status.paused": "一時停止中...",
        # ========================================
        # File Status
        # ========================================
        "file_status.pending": "待機中",
        "file_status.processing": "処理中",
        "file_status.success": "完了",
        "file_status.error": "エラー",
        "file_status.already_added": "追加済",
        "file_status.unsupported": "非対応",
        "file_status.added": "追加",
        # ========================================
        # Notification Messages
        # ========================================
        "notify.files_added": "{count}枚の画像が追加されました",
        "notify.files_skipped": "(スキップ: {count}件)",
        "notify.files_error": "(エラー: {count}件)",
        "notify.files_removed": "{count}枚の画像が削除されました",
        "notify.all_files_cleared": "すべての画像が削除されました",
        "notify.no_files_to_convert": "変換するファイルがありません",
        # ========================================
        # Error Messages - Validators
        # ========================================
        "error.file_not_exist": "ファイルが存在しません",
        "error.not_a_file": "ファイルではありません",
        "error.unsupported_format": "非対応フォーマット: {suffix}",
        "error.image_corrupted": "画像ファイルが破損しています: {detail}",
        "error.quality_range": "{format}の品質は0-100の範囲で指定してください",
        "error.png_compress_range": "PNGの圧縮レベルは0-9の範囲で指定してください",
        "error.resize_value_min": "リサイズ値は1以上を指定してください",
        "error.percentage_max": "パーセンテージは500%以下で指定してください",
        "error.pixel_max": "ピクセル値は50000以下で指定してください",
        "error.output_path_empty": "出力先パスを指定してください",
        "error.output_parent_not_exist": "出力先の親ディレクトリが存在しません",
        "error.invalid_path": "パスが無効です: {detail}",
        "error.info_retrieval_failed": "エラー: 情報取得失敗",
        "error.generic": "エラー: {message}",
        # ========================================
        # Error Messages - Processing
        # ========================================
        "error.unsupported_format_processing": "未対応のフォーマット: {format}",
        "error.numbering_failed": "連番サフィックス生成失敗: {file}",
        "error.folder_creation_failed": "フォルダ作成失敗: {detail}",
        # ========================================
        # Log Messages
        # ========================================
        "log.conversion_start": "=== 変換開始 ===",
        "log.conversion_complete": "=== 変換完了 ===",
        "log.total_files": "合計",
        "log.original_size": "変換前サイズ",
        "log.converted_size": "変換後サイズ",
        "log.reduction_size": "削減サイズ",
        "log.reduction_rate": "削減率",
        "log.file_processing": "[{index}/{total}] {filename}",
        "log.file_success": "  → 成功: {original} → {converted} (削減: {reduction}, {percentage}%)",
        "log.file_error": "  → エラー: {error}",
        "log.file_cancelled": "  → キャンセル",
    },
    LANG_ENGLISH: {
        # ========================================
        # Toolbar
        # ========================================
        "toolbar.menu": "Menu",
        "toolbar.add_files": "Add Files",
        "toolbar.add_folder": "Add Folder",
        "toolbar.clear_all": "Clear All",
        "toolbar.start": "Start",
        "toolbar.pause": "Pause",
        "toolbar.resume": "Resume",
        "toolbar.stop": "Stop",
        "toolbar.settings": "Settings",
        "toolbar.about": "About",
        # ========================================
        # File List
        # ========================================
        "filelist.column.filename": "File Name",
        "filelist.column.resolution": "Resolution",
        "filelist.column.size": "Size",
        "filelist.column.modified": "Modified",
        "filelist.column.folder": "Folder Path",
        "filelist.drop_hint": "Drag & drop files",
        "filelist.context.add_files": "Add Files",
        "filelist.context.add_folder": "Add Folder",
        "filelist.context.remove_selected": "Remove Selected",
        "filelist.context.remove_others": "Remove Others",
        "filelist.context.clear_all": "Clear All",
        "filelist.context.open_folder": "Open Folder",
        "filelist.context.load_same_folder": "Load All Images from Same Folder",
        # ========================================
        # Settings Panel - Sections
        # ========================================
        "settings.section.output_format": "Output Format",
        "settings.section.resize": "Resize",
        "settings.section.output_path": "Output Path",
        # ========================================
        # Settings Panel - Format Options
        # ========================================
        "settings.format.webp": "WebP",
        "settings.format.png": "PNG",
        "settings.format.jpg": "JPG",
        "settings.format.bmp": "BMP",
        # ========================================
        # Settings Panel - WebP Options
        # ========================================
        "settings.webp.quality": "Quality",
        "settings.webp.quality_note": "Quality 100 automatically becomes lossless",
        "settings.webp.method": "Compression Method",
        "settings.webp.method_note": "0=Fast (larger), 6=Slow (smaller)",
        # ========================================
        # Settings Panel - PNG Options
        # ========================================
        "settings.png.compress_level": "Compression Level",
        "settings.png.compress_level_note": "0=No compression (fast), 9=Maximum compression (slow)",
        "settings.png.optimize": "Optimize",
        "settings.png.optimize_enable": "Enable",
        "settings.png.optimize_note": "Reduces file size, increases processing time",
        # ========================================
        # Settings Panel - JPG Options
        # ========================================
        "settings.jpg.quality": "Quality",
        "settings.jpg.quality_note": "0=Lowest quality, 100=Highest quality",
        "settings.jpg.subsampling": "Subsampling",
        "settings.jpg.progressive": "Progressive",
        "settings.jpg.progressive_enable": "Enable",
        "settings.jpg.transparent_bg": "Transparent Background Color",
        # ========================================
        # Settings Panel - BMP Options
        # ========================================
        "settings.bmp.no_options": "No options available",
        # ========================================
        # Settings Panel - Resize Options
        # ========================================
        "settings.resize.enable": "Enable Resize",
        "settings.resize.mode": "Mode",
        "settings.resize.mode.ratio": "Ratio",
        "settings.resize.mode.pixels": "Pixels",
        "settings.resize.mode.long_edge": "Long Edge",
        "settings.resize.mode.short_edge": "Short Edge",
        "settings.resize.percentage": "Percentage",
        "settings.resize.percentage_unit": "%",
        "settings.resize.width": "Width",
        "settings.resize.height": "Height",
        "settings.resize.edge_value": "Edge Length",
        "settings.resize.px_unit": "px",
        # ========================================
        # Settings Panel - Output Path
        # ========================================
        "settings.output.path": "Output Path",
        "settings.output.browse": "Browse",
        "settings.output.default_note": "Default: Create ./converted/ in source folder",
        "settings.output.relative_note": "Relative path (output to same level as source)",
        "settings.output.numbering": "Numbering Suffix",
        "settings.output.numbering_enable": "Enable",
        "settings.output.numbering_note": "Add _001, _002... when file exists",
        "settings.output.keep_metadata": "Keep Metadata",
        "settings.output.keep_metadata_enable": "Enable",
        # ========================================
        # Settings Screen
        # ========================================
        "settings_screen.title": "Settings",
        "settings_screen.appearance": "Appearance",
        "settings_screen.language": "Language",
        "settings_screen.language.system": "System",
        "settings_screen.language.english": "English",
        "settings_screen.language.japanese": "日本語",
        "settings_screen.theme": "Theme",
        "settings_screen.theme.label": "Theme",
        "settings_screen.theme.system": "System",
        "settings_screen.theme.dark": "Dark",
        "settings_screen.theme.light": "Light",
        "settings_screen.behavior": "Behavior",
        "settings_screen.behavior.recursive": "Load subfolders",
        "settings_screen.behavior.overwrite_label": "When file exists",
        "settings_screen.behavior.overwrite_rename": "Save with numbering suffix (recommended)",
        "settings_screen.behavior.overwrite_yes": "Overwrite",
        "settings_screen.image_processing": "Image Processing",
        "settings_screen.image_processing.keep_metadata": "Keep metadata (Exif, etc.)",
        "settings_screen.image_processing.bg_color_label": "Background color for transparent images when converting to JPG",
        "settings_screen.image_processing.bg_color_dialog": "Select background color",
        "settings_screen.button.reset": " Reset to Defaults",
        "settings_screen.button.cancel": " Cancel",
        "settings_screen.button.save": " Save and Close",
        "settings_screen.close": "Close",
        "settings_screen.save": "Save",
        # ========================================
        # Dialogs
        # ========================================
        "dialog.confirm": "Confirm",
        "dialog.error": "Error",
        "dialog.info": "Information",
        "dialog.yes": "Yes",
        "dialog.no": "No",
        "dialog.ok": "OK",
        "dialog.cancel": "Cancel",
        "dialog.resume": "Resume",
        "dialog.stop": "Stop",
        "dialog.exit": "Exit",
        "dialog.pause.title": "Paused",
        "dialog.pause.message": "Conversion has been paused",
        "dialog.close.title": "Confirm",
        "dialog.close.message": "Conversion is in progress.\nExit anyway?",
        "dialog.reset.title": "Confirm",
        "dialog.reset.message": "Reset all settings to defaults?\n(Includes output format, resize, and quality settings)",
        "dialog.select_folder": "Select Folder",
        "dialog.select_files": "Select Image Files (Multiple Selection)",
        "dialog.select_output_folder": "Select Output Folder",
        "dialog.file_filter": "Image Files (*.webp *.png *.jpg *.jpeg *.bmp);;All Files (*.*)",
        "dialog.clear_all.message": "Remove all files?",
        "dialog.output_folder.title": "Select Output Folder",
        "dialog.about.title": "About",
        "dialog.about.version": "Version 1.0.3",
        "dialog.about.description": "A simple and efficient batch image converter",
        "dialog.about.license": "License: GNU General Public License v3.0",
        "dialog.about.author": "© 2026 Amatsukast",
        "dialog.about.close": "Close",
        # ========================================
        # Status Messages
        # ========================================
        "status.ready": "Ready",
        "status.no_files": "No images to process",
        "status.processing": "Processing: {current} / {total}",
        "status.stopped": "Stopped: Completed {success} / Cancelled {cancelled}",
        "status.completed": "Completed",
        "status.completed_all_failed": "Completed (All Failed)",
        "status.completed_with_errors": "Completed (With Errors)",
        "status.completed_detail": "{status}: Success {success} / Failed {error}",
        "status.paused": "Paused...",
        # ========================================
        # File Status
        # ========================================
        "file_status.pending": "Pending",
        "file_status.processing": "Processing",
        "file_status.success": "Success",
        "file_status.error": "Error",
        "file_status.already_added": "Already Added",
        "file_status.unsupported": "Unsupported",
        "file_status.added": "Added",
        # ========================================
        # Notification Messages
        # ========================================
        "notify.files_added": "{count} image(s) added",
        "notify.files_skipped": "(Skipped: {count})",
        "notify.files_error": "(Error: {count})",
        "notify.files_removed": "{count} image(s) removed",
        "notify.all_files_cleared": "All images cleared",
        "notify.no_files_to_convert": "No files to convert",
        # ========================================
        # Error Messages - Validators
        # ========================================
        "error.file_not_exist": "File does not exist",
        "error.not_a_file": "Not a file",
        "error.unsupported_format": "Unsupported format: {suffix}",
        "error.image_corrupted": "Image file is corrupted: {detail}",
        "error.quality_range": "{format} quality must be 0-100",
        "error.png_compress_range": "PNG compression level must be 0-9",
        "error.resize_value_min": "Resize value must be 1 or greater",
        "error.percentage_max": "Percentage must be 500% or less",
        "error.pixel_max": "Pixel value must be 50000 or less",
        "error.output_path_empty": "Please specify output path",
        "error.output_parent_not_exist": "Output parent directory does not exist",
        "error.invalid_path": "Invalid path: {detail}",
        "error.info_retrieval_failed": "Error: Failed to retrieve info",
        "error.generic": "Error: {message}",
        # ========================================
        # Error Messages - Processing
        # ========================================
        "error.unsupported_format_processing": "Unsupported format: {format}",
        "error.numbering_failed": "Failed to generate numbering suffix: {file}",
        "error.folder_creation_failed": "Failed to create folder: {detail}",
        # ========================================
        # Log Messages
        # ========================================
        "log.conversion_start": "=== Conversion Started ===",
        "log.conversion_complete": "=== Conversion Completed ===",
        "log.total_files": "Total",
        "log.original_size": "Original Size",
        "log.converted_size": "Converted Size",
        "log.reduction_size": "Reduction",
        "log.reduction_rate": "Reduction Rate",
        "log.file_processing": "[{index}/{total}] {filename}",
        "log.file_success": "  → Success: {original} → {converted} (Reduction: {reduction}, {percentage}%)",
        "log.file_error": "  → Error: {error}",
        "log.file_cancelled": "  → Cancelled",
    },
}

# Mapping from internal constants to translation keys for resize modes
RESIZE_MODE_TRANSLATION_KEYS = {
    RESIZE_MODE_RATIO: "settings.resize.mode.ratio",
    RESIZE_MODE_PIXELS: "settings.resize.mode.pixels",
    RESIZE_MODE_LONG_EDGE: "settings.resize.mode.long_edge",
    RESIZE_MODE_SHORT_EDGE: "settings.resize.mode.short_edge",
}

# Mapping from translation text back to internal constants (for UI -> Logic conversion)
# This will be populated dynamically based on current language
_REVERSE_RESIZE_MODE_MAP = {}


def get_resize_mode_display_name(mode: str, language: str = LANG_JAPANESE) -> str:
    """Get display name for resize mode"""
    key = RESIZE_MODE_TRANSLATION_KEYS.get(mode, "")
    return TRANSLATIONS[language].get(key, mode)


def get_resize_mode_from_display(
    display_name: str, language: str = LANG_JAPANESE
) -> str:
    """Convert display name back to internal constant"""
    for mode, key in RESIZE_MODE_TRANSLATION_KEYS.items():
        if TRANSLATIONS[language].get(key) == display_name:
            return mode
    return RESIZE_MODE_RATIO  # fallback


def translate(key: str, language: str = LANG_JAPANESE, **kwargs) -> str:
    """
    Get translated text by key

    Args:
        key: Translation key (e.g., "toolbar.start")
        language: Language code (LANG_JAPANESE or LANG_ENGLISH)
        **kwargs: Format parameters for string interpolation

    Returns:
        Translated text
    """
    text = TRANSLATIONS.get(language, TRANSLATIONS[LANG_JAPANESE]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text
