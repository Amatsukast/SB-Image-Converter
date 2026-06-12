"""
Tests for managers.settings_manager module (load/save/migration)
"""

import json
from pathlib import Path
from managers.settings_manager import SettingsManager, AppSettings


def _write_settings(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


class TestSettingsLoad:
    """Tests for settings loading"""

    def test_missing_file_returns_defaults(self, temp_dir: Path):
        """Missing settings file falls back to defaults"""
        manager = SettingsManager(settings_path=temp_dir / "none.json")

        assert manager.settings == AppSettings()

    def test_corrupted_file_returns_defaults(self, temp_dir: Path):
        """Corrupted JSON falls back to defaults"""
        path = temp_dir / "settings.json"
        path.write_text("{ not valid json", encoding="utf-8")

        manager = SettingsManager(settings_path=path)

        assert manager.settings == AppSettings()

    def test_unknown_keys_are_ignored(self, temp_dir: Path):
        """Keys removed in newer versions do not crash loading"""
        path = temp_dir / "settings.json"
        _write_settings(path, {"jpg_quality": 75, "removed_legacy_key": 123})

        manager = SettingsManager(settings_path=path)

        assert manager.settings.jpg_quality == 75


class TestTgaAlphaMigration:
    """Tests for v1.1.x tga_alpha -> tga_flatten migration"""

    def test_tga_alpha_true_becomes_flatten_false(self, temp_dir: Path):
        """tga_alpha=True (keep alpha) migrates to tga_flatten=False"""
        path = temp_dir / "settings.json"
        _write_settings(path, {"tga_alpha": True})

        manager = SettingsManager(settings_path=path)

        assert manager.settings.tga_flatten is False

    def test_tga_alpha_false_becomes_flatten_true(self, temp_dir: Path):
        """tga_alpha=False (drop alpha) migrates to tga_flatten=True"""
        path = temp_dir / "settings.json"
        _write_settings(path, {"tga_alpha": False})

        manager = SettingsManager(settings_path=path)

        assert manager.settings.tga_flatten is True

    def test_existing_tga_flatten_wins_over_tga_alpha(self, temp_dir: Path):
        """If both keys exist, tga_flatten takes precedence"""
        path = temp_dir / "settings.json"
        _write_settings(path, {"tga_alpha": True, "tga_flatten": True})

        manager = SettingsManager(settings_path=path)

        assert manager.settings.tga_flatten is True

    def test_saved_settings_drop_tga_alpha(self, temp_dir: Path):
        """Re-saving migrated settings writes tga_flatten, not tga_alpha"""
        path = temp_dir / "settings.json"
        _write_settings(path, {"tga_alpha": False})

        manager = SettingsManager(settings_path=path)
        manager.save()

        data = json.loads(path.read_text(encoding="utf-8"))
        assert "tga_alpha" not in data
        assert data["tga_flatten"] is True
