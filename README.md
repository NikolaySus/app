# ДЗ2 ТРПО
### Row data gateway + Domain model
```
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
```
