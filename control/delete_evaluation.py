"""
Module with control class DeleteEvaluation implementation.
"""
from control.run_evaluation import RunEvaluation
from persistence.eval_gateway import EvalGateway


class DeleteEvaluation:
    """
    Control class.
    """
    def delete_eval(self, eval_id: int):
        """
        Select evaluation by eval_id, may be running.
        """
        try:
            RunEvaluation.stop_eval(eval_id)
        except KeyError:
            pass
        gateway = EvalGateway(eval_id)
        gateway.delete()
