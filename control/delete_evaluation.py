"""
Модуль с реализацией управляющего класса DeleteEvaluation.
"""
from control.run_evaluation import RunEvaluation
from persistence.eval_gateway import EvalGateway


class DeleteEvaluation:
    """
    Управляющий класс.
    """
    def delete_eval(self, eval_id: int):
        """
        Выбор оценки по идентификатору, может выполняться.
        """
        try:
            RunEvaluation.stop_eval(eval_id)
        except KeyError:
            pass
        gateway = EvalGateway(eval_id)
        gateway.delete()
