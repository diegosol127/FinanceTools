The directoy structure of this project is broken down into folders, each one tied to a specific repository to make this project secure and easily replicable. The general file structure can be seen in the depiction below.

```bash
FinanceManager/
├── repo/                  # Git repository (code only)
│   ├── src/               # Python source code
│   │   ├── ingest/        # CSV ingestion & parsers
│   │   ├── normalize/     # Cleaning & normalization logic
│   │   ├── categorize/    # Merchant & category engine
│   │   ├── export/        # HTML / report generation
│   │   └── main.py
│   ├── rules/             # JSON/YAML categorization rules
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
└── data/                  # NOT tracked by Git (symlinked)
    ├── incoming/          # New CSV files dropped here
    ├── archive/           # Immutable raw CSV archive
    ├── backups/           # Encrypted snapshots
    ├── exports/           # Generated HTML / reports
    └── budget.db          # SQLite database
```

The `repo` folder is a clone of the Git repository associated with the project. Currently, that repository is `https://github.com/diegosol127/FinanceTools` on the `dev/overhaul` branch. The purpose of the files in this repo are exclusively for ingesting, parsing, analyzing, exporting the data located in the `data` folder. At no point should any financial data flow through this repository.
