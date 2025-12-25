"""
Module with control class RunEvaluation implementation.
"""
import threading
import time

from domain.evaluation import Evaluation
from persistence.eval_gateway import EvalGateway
from util.singleton import Singleton


class RunEvaluation(metaclass=Singleton):
    """
    Control class.
    """
    _running_evaluations = dict()

    @classmethod
    def run_eval(cls, evaluation: Evaluation):
        """
        Run evaluation.
        """
        eval_id = evaluation.get_eval_id()
        assert eval_id not in cls._running_evaluations, "Already running"
        evaluation.start_eval()
        thread = threading.Thread(target=cls._run_eval_async,
                                  daemon=True, args=(eval_id,))
        is_stopped = threading.Event()
        cls._running_evaluations[eval_id] = (evaluation, is_stopped)
        thread.start()

    @classmethod
    def _run_eval_async(cls, eval_id: int):
        """
        Run the evaluation asynchronously for 5 seconds.
        """
        pair = cls._running_evaluations[eval_id]
        evaluation = pair[0]
        is_stopped = pair[1]
        for i in range(5):
            time.sleep(1)
            evaluation.append_results(f"Step {i+1} completed\n")
            if is_stopped.is_set():
                break
        evaluation.stop_eval()
        gateway = EvalGateway(
            evaluation.get_eval_id(),
            evaluation.get_eval_name(),
            evaluation.get_eval_start_timestamp(),
            evaluation.get_eval_finish_timestamp(),
            evaluation.get_eval_state(),
            evaluation.get_eval_results()
        )
        gateway.update()
        cls._running_evaluations.pop(eval_id)

    @classmethod
    def get_running_evaluation_by_id(cls, eval_id: int):
        """
        Get evaluation if it is running.
        """
        return cls._running_evaluations[eval_id][0]

    @classmethod
    def stop_eval(cls, eval_id: int):
        """
        Stop evaluation if it is running.
        """
        cls._running_evaluations[eval_id][1].set()
