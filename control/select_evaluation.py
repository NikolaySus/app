"""
Module with control class SelectEvaluation implementation.
"""
from control.run_evaluation import RunEvaluation
from persistence.eval_finder import EvalFinder


class SelectEvaluation:
    """
    Control class.
    """
    def select_eval_by_name(self, eval_name: str):
        """
        Select evaluations by names starting with eval_name prefix.
        """
        finder = EvalFinder()
        return finder.find_eval_by_name(eval_name)

    def select_eval_by_id(self, eval_id: int):
        """
        Select evaluation by eval_id, may be running.
        """
        try:
            return RunEvaluation.get_running_evaluation_by_id(eval_id)
        except KeyError:
            finder = EvalFinder()
            return finder.find_eval(eval_id)
