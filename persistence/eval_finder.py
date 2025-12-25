"""
Module with finder class EvalFinder implementation.
"""
from database.db import get_connection
from domain.evaluation import Evaluation


class EvalFinder:
    """
    Finder class.
    """
    def find_eval(self, eval_id: int):
        """
        Search by id for UI select.
        """
        conn = get_connection()
        cursor = conn.cursor()

        row = cursor.execute(
            "SELECT * FROM Eval WHERE eval_id = ?",
            (eval_id,)
        ).fetchone()

        conn.close()
        return self._row_to_eval(row)

    def find_eval_by_name(self, eval_name: str):
        """
        Prefix search for UI list.
        """
        conn = get_connection()
        cursor = conn.cursor()

        rows = cursor.execute(
            "SELECT * FROM Eval WHERE eval_name LIKE ? ORDER BY eval_name",
            (eval_name + "%",)
        ).fetchall()

        conn.close()
        return [self._row_to_eval(row) for row in rows]

    def _row_to_eval(self, row):
        if row is None:
            return None

        return Evaluation(
            eval_id=row["eval_id"],
            eval_name=row["eval_name"],
            eval_start_timestamp=row["eval_start_timestamp"],
            eval_finish_timestamp=row["eval_finish_timestamp"],
            eval_state=row["eval_state"],
            eval_results=row["eval_results"]
        )
