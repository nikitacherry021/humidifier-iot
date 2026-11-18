"""Хранилище настроек в JSON-файле.

Переживает перезапуск сервера: контроллер читает настройки при старте
и записывает при изменении через API.
"""
import json
import os

# storage/settings.json относительно корня проекта
DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "storage",
    "settings.json",
)

DEFAULTS = {
    "mode": "auto",
    "on_below": 45.0,
    "off_above": 55.0,
}


class SettingsStore:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path

    def load(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return dict(DEFAULTS)
        merged = dict(DEFAULTS)
        merged.update({k: data[k] for k in DEFAULTS if k in data})
        return merged

    def save(self, settings: dict) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        payload = {k: settings[k] for k in DEFAULTS if k in settings}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
