"""
app/
│
├── main.py
│
├── ui/                 # Boundary
│   └── evaluation_ui.py
│
├── control/            # Control
│   ├── create_evaluation.py
│   ├── select_evaluation.py
│   ├── run_evaluation.py
│   ├── delete_evaluation.py
│   └── get_evaluation_report.py
│
├── domain/             # Domain model
│   └── evaluation.py
│
├── persistence/        # Row data gateway
│   ├── eval_gateway.py
│   └── eval_finder.py
│
├── database/
│   └── db.py           # Sqlite connection + schema
│
└── util/               # Helpers
    ├── singleton.py
    ├── translation_manager.py
    └── report_exporter.py
"""
import sys

from PyQt6.QtWidgets import QApplication

from ui.evaluation_ui import EvaluationUI


def main():
    app = QApplication(sys.argv)
    ui = EvaluationUI()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# │   ├── __init__.py
