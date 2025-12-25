"""
Module with domain class Evaluation implementation.
"""
from datetime import datetime


class Evaluation:
    """
    Domain class.
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
        Setter for eval_id.
        """
        self.eval_id = eval_id

    def set_name(self, name: str):
        """
        Setter for eval_name.
        """
        self.eval_name = name

    def start_eval(self):
        """
        Domain logic for evaluation start.
        """
        self.eval_state = "RUNNING"
        self.eval_start_timestamp = datetime.now().isoformat()
        self.eval_results = ""

    def append_results(self, delta):
        """
        Domain logic for evaluation results increment.
        """
        self.eval_results += delta

    def stop_eval(self, results: str = None):
        """
        Domain logic for evaluation stop.
        """
        self.eval_state = "FINISHED"
        self.eval_finish_timestamp = datetime.now().isoformat()
        if results is not None:
            self.eval_results = results

    def get_state_timestamps(self):
        """
        Getter for eval_state, eval_start_timestamp and
        eval_finish_timestamp retrieval.
        """
        return {
            "state": self.eval_state,
            "start": self.eval_start_timestamp,
            "finish": self.eval_finish_timestamp
        }

    def get_eval_id(self):
        """
        Getter for eval_id retrieval.
        """
        return self.eval_id

    def get_eval_name(self):
        """
        Getter for eval_name retrieval.
        """
        return self.eval_name

    def get_eval_start_timestamp(self):
        """
        Getter for eval_start_timestamp retrieval.
        """
        return self.eval_start_timestamp

    def get_eval_finish_timestamp(self):
        """
        Getter for eval_finish_timestamp retrieval.
        """
        return self.eval_finish_timestamp

    def get_eval_state(self):
        """
        Getter for eval_state retrieval.
        """
        return self.eval_state

    def get_eval_results(self):
        """
        Getter for eval_results retrieval.
        """
        return self.eval_results
