"""
Модуль с реализацией управляющего класса SelectEvaluation.
"""
from control.run_evaluation import RunEvaluation
from persistence.eval_finder import EvalFinder


class SelectEvaluation:
    """
    Управляющий класс.
    """
    def select_eval_by_name(self, eval_name: str):
        """
        Выбор оценок по именам, начинающимся с префикса eval_name.
        """
        finder = EvalFinder()
        return finder.find_eval_by_name(eval_name)

    def select_eval_by_id(self, eval_id: int):
        """
        Выбор оценки по идентификатору, может выполняться.
        """
        try:
            return RunEvaluation.get_running_evaluation_by_id(eval_id)
        except KeyError:
            finder = EvalFinder()
            return finder.find_eval(eval_id)
