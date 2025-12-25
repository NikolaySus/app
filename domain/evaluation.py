"""
Модуль с реализацией доменного класса Evaluation.
"""
from datetime import datetime


class Evaluation:
    """
    Доменный класс.
    """
    def __init__(
        self,
        eval_id=None,
        eval_name=None,
        eval_start_timestamp=None,
        eval_finish_timestamp=None,
        eval_state="NEW",
        eval_results=None
    ):
        self.eval_id = eval_id
        self.eval_name = eval_name
        self.eval_start_timestamp = eval_start_timestamp
        self.eval_finish_timestamp = eval_finish_timestamp
        self.eval_state = eval_state
        self.eval_results = eval_results
        self._eval_thread = None

    def set_id(self, eval_id):
        """
        Установщик для идентификатора оценки.
        """
        self.eval_id = eval_id

    def set_name(self, name: str):
        """
        Установщик для имени оценки.
        """
        self.eval_name = name

    def start_eval(self):
        """
        Доменная логика для начала оценки.
        """
        self.eval_state = "RUNNING"
        self.eval_start_timestamp = datetime.now().isoformat()
        self.eval_results = ""

    def append_results(self, delta):
        """
        Доменная логика для увеличения результатов оценки.
        """
        self.eval_results += delta

    def stop_eval(self, results: str = None):
        """
        Доменная логика для остановки оценки.
        """
        self.eval_state = "FINISHED"
        self.eval_finish_timestamp = datetime.now().isoformat()
        if results is not None:
            self.eval_results = results

    def get_state_timestamps(self):
        """
        Получение состояния, времени начала и времени окончания оценки.
        """
        return {
            "state": self.eval_state,
            "start": self.eval_start_timestamp,
            "finish": self.eval_finish_timestamp
        }

    def get_eval_id(self):
        """
        Получение идентификатора оценки.
        """
        return self.eval_id

    def get_eval_name(self):
        """
        Получение имени оценки.
        """
        return self.eval_name

    def get_eval_start_timestamp(self):
        """
        Получение времени начала оценки.
        """
        return self.eval_start_timestamp

    def get_eval_finish_timestamp(self):
        """
        Получение времени окончания оценки.
        """
        return self.eval_finish_timestamp

    def get_eval_state(self):
        """
        Получение состояния оценки.
        """
        return self.eval_state

    def get_eval_results(self):
        """
        Получение результатов оценки.
        """
        return self.eval_results
