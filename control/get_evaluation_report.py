"""
Module with control class GetEvaluationReport implementation.
"""
class GetEvaluationReport:
    """
    Control class.
    """
    def get_eval_report(self, evaluation):
        """
        Get evaluation results.
        """
        return evaluation.get_eval_results()

    def export_eval_report_to_file(self, evaluation, filename: str):
        """
        Write evaluation results to file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(evaluation.get_eval_results() or "")
