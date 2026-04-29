"""
Translation Manager

Centralized translation management for GUI layer.
Provides language switching and UI refresh capabilities.
"""

from PySide6.QtCore import QObject, Signal, QLocale
from config.constants import LANG_SYSTEM, LANG_JAPANESE, LANG_ENGLISH
from config.translations import (
    translate,
    TRANSLATIONS,
    get_resize_mode_display_name,
    get_resize_mode_from_display,
)


class TranslationManager(QObject):
    """
    Translation manager for GUI layer

    Manages current language and notifies UI components when language changes.
    """

    # Signal emitted when language changes
    language_changed = Signal(str)  # new language code

    _instance = None

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize translation manager"""
        if self._initialized:
            return

        super().__init__()
        self._current_language = self._detect_system_language()
        self._initialized = True

    def _detect_system_language(self) -> str:
        """
        Detect system language

        Returns:
            Language code (LANG_JAPANESE or LANG_ENGLISH)
        """
        system_locale = QLocale.system().name()  # e.g., "ja_JP", "en_US"
        language_code = system_locale.split("_")[0]  # Extract "ja" or "en"

        if language_code == "ja":
            return LANG_JAPANESE
        else:
            return LANG_ENGLISH  # Fallback to English

    @property
    def current_language(self) -> str:
        """Get current language code"""
        return self._current_language

    def set_language(self, language_code: str) -> None:
        """
        Set current language

        Args:
            language_code: Language code (LANG_SYSTEM, LANG_JAPANESE, or LANG_ENGLISH)
        """
        # If "system", detect actual system language
        if language_code == LANG_SYSTEM:
            actual_language = self._detect_system_language()
        else:
            actual_language = language_code

        if actual_language not in TRANSLATIONS:
            return

        if self._current_language != actual_language:
            self._current_language = actual_language
            self.language_changed.emit(actual_language)

    def tr(self, key: str, **kwargs) -> str:
        """
        Translate a key to current language

        Args:
            key: Translation key
            **kwargs: Format parameters

        Returns:
            Translated text
        """
        return translate(key, self._current_language, **kwargs)

    def get_available_languages(self) -> list:
        """
        Get list of available languages

        Returns:
            List of tuples: [(language_code, display_name_key), ...]
        """
        return [
            (LANG_SYSTEM, "settings_screen.language.system"),
            (LANG_ENGLISH, "settings_screen.language.english"),
            (LANG_JAPANESE, "settings_screen.language.japanese"),
        ]

    def get_resize_mode_display(self, mode: str) -> str:
        """
        Get display name for resize mode constant

        Args:
            mode: Internal resize mode constant

        Returns:
            Localized display name
        """
        return get_resize_mode_display_name(mode, self._current_language)

    def get_resize_mode_constant(self, display_name: str) -> str:
        """
        Convert display name to internal constant

        Args:
            display_name: Localized display name

        Returns:
            Internal resize mode constant
        """
        return get_resize_mode_from_display(display_name, self._current_language)


# Global singleton instance
_manager = None


def get_translation_manager() -> TranslationManager:
    """
    Get global translation manager instance

    Returns:
        TranslationManager singleton
    """
    global _manager
    if _manager is None:
        _manager = TranslationManager()
    return _manager
