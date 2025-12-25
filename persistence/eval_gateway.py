"""
Module with gateway class EvalGateway implementation.
"""
from database.db import get_connection


class EvalGateway:
    """
    Gateway class.
    """
    def __init__(
        self,
        eval_id=None,
        eval_name=None,
        eval_start_timestamp=None,
        eval_finish_timestamp=None,
        eval_state=None,
        eval_results=None
    ):
        self._eval_id = eval_id
        self._eval_name = eval_name
        self._eval_start_timestamp = eval_start_timestamp
        self._eval_finish_timestamp = eval_finish_timestamp
        self._eval_state = eval_state
        self._eval_results = eval_results

    def get_id(self):
        """
        Getter for _eval_id retrieval.
        """
        return self._eval_id

    def get_name(self):
        """
        Getter for _eval_name retrieval.
        """
        return self._eval_name

    def get_start_timestamp(self):
        """
        Getter for _eval_start_timestamp retrieval.
        """
        return self._eval_start_timestamp

    def get_finish_timestamp(self):
        """
        Getter for _eval_finish_timestamp retrieval.
        """
        return self._eval_finish_timestamp

    def get_state(self):
        """
        Getter for _eval_state retrieval.
        """
        return self._eval_state

    def get_results(self):
        """
        Getter for _eval_results retrieval.
        """
        return self._eval_results

    def set_id(self, eval_id):
        """
        Setter for _eval_id.
        """
        self._eval_id = eval_id

    def set_name(self, name):
        """
        Setter for _eval_name.
        """
        self._eval_name = name

    def set_start_timestamp(self, ts):
        """
        Setter for _eval_start_timestamp.
        """
        self._eval_start_timestamp = ts

    def set_finish_timestamp(self, ts):
        """
        Setter for _eval_finish_timestamp.
        """
        self._eval_finish_timestamp = ts

    def set_state(self, state):
        """
        Setter for _eval_state.
        """
        self._eval_state = state

    def set_results(self, results):
        """
        Setter for _eval_results.
        """
        self._eval_results = results

    def insert(self):
        """
        Row data gateway insert for database.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Eval (
                eval_name,
                eval_start_timestamp,
                eval_finish_timestamp,
                eval_state,
                eval_results
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            self._eval_name,
            self._eval_start_timestamp,
            self._eval_finish_timestamp,
            self._eval_state,
            self._eval_results
        ))

        self._eval_id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update(self):
        """
        Row data gateway update for database.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Eval SET
                eval_name = ?,
                eval_start_timestamp = ?,
                eval_finish_timestamp = ?,
                eval_state = ?,
                eval_results = ?
            WHERE eval_id = ?
        """, (
            self._eval_name,
            self._eval_start_timestamp,
            self._eval_finish_timestamp,
            self._eval_state,
            self._eval_results,
            self._eval_id
        ))

        conn.commit()
        conn.close()

    def delete(self):
        """
        Row data gateway delete for database.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Eval WHERE eval_id = ?",
            (self._eval_id,)
        )

        conn.commit()
        conn.close()
