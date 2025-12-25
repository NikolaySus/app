"""
Модуль для TranslationManager.
"""
from util.singleton import Singleton


class TranslationManager(metaclass=Singleton):
    """
    Простой менеджер переводов, предоставляющий строки перевода.
    """
    _translations = {
        "en": {
            "window_title": "Embedding Model Benchmark",
            "search_placeholder": "Search evaluations...",
            "name_placeholder": "Name new evaluation...",
            "create_btn": "Create",
            "run_btn": "Run",
            "stop_btn": "Stop",
            "delete_btn": "Delete",
            "ui_settings_label": "UI settings:",
            "created_msg": "Evaluation created",
            "running_msg": "Evaluation started",
            "finished_msg": "Evaluation stopped",
            "deleted_msg": "Evaluation deleted",
            "invalid_name": "Invalid name",
            "not_running": "Not running",
            "state_label": "-"
        },
        "ru": {
            "window_title": "Бенчмарк моделей эмбеддинга",
            "search_placeholder": "Поиск оценок...",
            "name_placeholder": "Название новой оценки...",
            "create_btn": "Создать",
            "run_btn": "Запустить",
            "stop_btn": "Остановить",
            "delete_btn": "Удалить",
            "ui_settings_label": "UI настройки:",
            "created_msg": "Оценка создана",
            "running_msg": "Оценка запущена",
            "finished_msg": "Оценка остановлена",
            "deleted_msg": "Оценка удалена",
            "invalid_name": "Неверное имя",
            "not_running": "Не запущено",
            "state_label": "-"
        }
    }

    _current_lang = "ru"

    @classmethod
    def switch_language(cls, lang_name: str):
        """Переключение языка на основе названия языка."""
        if lang_name == "English":
            cls._current_lang = "en"
        elif lang_name == "Русский":
            cls._current_lang = "ru"

    @classmethod
    def tr(cls, key: str) -> str:
        """Получение перевода для данного ключа."""
        return cls._translations[cls._current_lang].get(key, key)
