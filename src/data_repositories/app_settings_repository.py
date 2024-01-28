import pathlib

from src.models.app_settings_model import AppSettingsModel


class AppSettingsRepository:
    def _get_root(self) -> str:
        return pathlib.Path(__file__).parent.parent.parent

    def get_settings(self):
        root = self._get_root()
        with open(f"{root}/data/app_settings.json", "r", encoding="utf-8") as f:
            settings_json = f.read()
        app_settings = AppSettingsModel.model_validate_json(settings_json)

        return app_settings
