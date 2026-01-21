import argparse
import sys
from pathlib import Path
from datetime import datetime
from src.core.db import DIR_DATA, PATH_DB, init_db

DIR_INCOMING = DIR_DATA / "incoming"

def handle_ingest(args):
    print("Running ingest step...")
    # TODO: call ingest pipeline

def handle_categorize(args):
    print("Running categorize step...")
    # TODO: call categorize pipeline

def handle_export(args):
    print("Running export step...")
    # TODO: call export pipeline

def handle_status(args):
    print("FinanceManager status:")
    init_db()
    print(f"Database ready at {PATH_DB}")

    # --- Incoming CSVs ---
    if DIR_INCOMING.exists():
        csv_count = len(list(DIR_INCOMING.glob("*.csv")))
        print(f"Incoming CSV files: {csv_count}")
    else:
        print("Incoming CSV directory: missing")

    # --- Timestamp ---
    print(f"Checked at: {datetime.now().astimezone().strftime('%Y-%m-%d at %H:%M:%S')}")

    # print("- Database: TODO")
    # print("- Pending CSVs: TODO")
    # print("- Last run: TODO")

def build_parser():
    parser = argparse.ArgumentParser(
        prog = "financemanager",
        description = "Personal finance ingestion and analysis tool"
    )

    subparsers = parser.add_subparsers(
        title = "commands",
        dest = "command",
        required = True
    )
 
    # Ingest
    subparser_ingest = subparsers.add_parser(
        "ingest",
        help = "Ingest new CSV files into the database"
    )
    subparser_ingest.set_defaults(func = handle_ingest)

    # Categorize
    subparser_categorize = subparsers.add_parser(
        "categorize",
        help = "Apply merchant and category rules"
    )
    subparser_categorize.set_defaults(func = handle_categorize)

    # Export
    subparser_export = subparsers.add_parser(
        "export",
        help = "Generate reports and visualization"
    )
    subparser_export.set_defaults(func = handle_export)

    # Status
    subparser_status = subparsers.add_parser(
        "status",
        help = "Show system and data status"
    )
    subparser_status.set_defaults(func = handle_status)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
