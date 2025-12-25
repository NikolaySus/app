"""
Модуль с реализацией управляющего класса GetEvaluationReport.
"""
class GetEvaluationReport:
    """
    Управляющий класс.
    """
    def get_eval_report(self, evaluation):
        """
        Получение результатов оценки.
        """
        return evaluation.get_eval_results()

    def export_eval_report_to_file(self, evaluation, filename: str):
        """
        Запись результатов оценки в файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(evaluation.get_eval_results() or "")
