# Project Structure

The directoy structure of this project is broken down into folders, each one tied to a specific repository to make this project secure and easily replicable. The general file structure can be seen in the depiction below.

```bash
FinanceManager/            # Git repository (code only)
├── data/                  # NOT tracked by Git (symlinked)
│   ├── incoming/          # New CSV files dropped here
│   ├── archive/           # Immutable raw CSV archive
│   ├── backups/           # Encrypted snapshots
│   ├── exports/           # Generated HTML / reports
│   ├── rules/             # JSON/YAML categorization rules
│   └── budget.db          # SQLite database
└── src/                   # Python source code
    ├── core/              # SQLite code module
    │   ├── db.py          # SQLite connection and scehema
    │   └── models.py      # Canonical definitions
    ├── ingest/            # CSV ingestion & parsers
    ├── normalize/         # Cleaning & normalization logic
    ├── categorize/        # Merchant & category engine
    ├── export/            # HTML / report generation
    ├── main.py
    ├── build.sh
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    ├── run.sh
    └── .gitignore
```

The `repo` folder is a clone of the Git repository associated with the project. Currently, that repository is `https://github.com/diegosol127/FinanceTools` on the `dev/overhaul` branch. The purpose of the files in this repo are exclusively for ingesting, parsing, analyzing, exporting the data located in the `data` folder. At no point should any financial data flow through this repository.

The `data` folder is linked to a cloud drive used for storing data for processing, exporting, and backups. OneDrive is currently being used for this storage drive, and the `data` folder points to the OneDrive directory `OneDrive\Documents\Projects\FinanceManager\data` via a symlink. This project assumes the directory for OneDrive is `~/OneDrive` for both Windows and Linux.

# Setup

Follow these steps to set up your environment on either Windows or Linux.


1. Clone the git repository using SSH using the absolute path.

```bash
git clone -b dev/overhaul git@github.com:diegosol127/FinanceTools.git ~/Projects/FinanceManager
```

2. Create and symlink the data folder

**Windows**

Run the following commands from a powershell prompt with administative privileges. 

```pwsh
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\Projects\FinanceManager\data" -Target "$env:USERPROFILE\OneDrive\Documents\Projects\FinanceManager\data"
```

**Linux**

```bash
ln -s ~/OneDrive/FinanceManager/data ~/Projects/FinanceManager/data
```

**WSL**

```bash
WINUSER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
ln -s /mnt/c/Users/$WINUSER/OneDrive/Documents/Projects/FinanceManager/data ~/Projects/FinanceManager/data
```

3. Enter the repo and give executable permission to `build.sh` and `run.sh`

```bash
cd FinanceManager
chmod +x build.sh
chmod +x run.sh
```

4. Build the docker image (assumes Docker Desktop is already installed).

```bash
./build.sh
```

Rebuilding the image is necessary if any of the following files are changed:
- `Dockerfile`
- `requirements.txt`
- Anything in `src/`

5. Run the project

```bash
./run.sh
```

# Future Work

- [ ] Bootstrap installation and symlinking with bash scripts
