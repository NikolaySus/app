"""
Module with control class CreateEvaluation implementation.
"""
import re
from domain.evaluation import Evaluation
from persistence.eval_gateway import EvalGateway
from persistence.eval_finder import EvalFinder


class CreateEvaluation:
    """
    Control class.
    """
    def check_eval_name_input(self, eval_name: str):
        """
        Name validation.
        """
        if not eval_name:
            raise ValueError("Evaluation name cannot be empty")

        if len(eval_name) < 3:
            raise ValueError("Evaluation name must be at least 3 characters")

        # Allow only safe, simple characters
        if not re.match(r"^[A-Za-z0-9_\- ]+$", eval_name):
            raise ValueError(
                "Evaluation name contains invalid characters"
            )

        # Optional but very good: uniqueness check
        finder = EvalFinder()
        if finder.find_eval_by_name(eval_name):
            raise ValueError("Evaluation name already exists")

    def create_eval(self, eval_name: str):
        """
        Evaluation creation.
        """
        # Application-level validation
        self.check_eval_name_input(eval_name)

        evaluation = Evaluation(eval_name=eval_name)
        gateway = EvalGateway(
            evaluation.get_eval_id(),
            evaluation.get_eval_name(),
            evaluation.get_eval_start_timestamp(),
            evaluation.get_eval_finish_timestamp(),
            evaluation.get_eval_state(),
            evaluation.get_eval_results()
        )
        gateway.update()
        gateway.insert()
        evaluation.set_id(gateway.get_id())

        return evaluation
