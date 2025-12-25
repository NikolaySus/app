"""
Module with control class GetEvaluationReport implementation.
"""
class GetEvaluationReport:
    """
    Control class.
    """
    def get_eval_report(self, evaluation):
        return evaluation.eval_results

    def export_eval_report_to_file(self, evaluation, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(evaluation.eval_results or "")
