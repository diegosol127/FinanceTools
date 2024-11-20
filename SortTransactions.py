# Import Python libraries
import argparse
import os
import sys
import numpy as np
import pandas as pd

# Import custom libraries
from Utilities.parser import CSV
from Utilities.parser import JSON
from Utilities.interface import Interface

#===================================================================================================

# Identify a category for the given transaction
def group_transactions(description, classification_dict):
    for category, keywords in classification_dict.items():
        for keyword in keywords:
            if keyword.upper() in description.upper():
                return category
    return '***Unlabelled***'

# Extract the csv data from the selected directory
def extract_data(directory,date):
    df_combined = pd.DataFrame()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if date in file:
                file_path = os.path.join(root, file)
                try:
                    csv_parser = CSV()
                    df = csv_parser.parse_file(file_path)
                    df_combined = pd.concat([df_combined,df],axis=0, ignore_index=True)
                    print(f"Processed {file_path}")
                except ValueError as e:
                    print(e)
    df_combined.sort_values(by='DATE', inplace=True)
    df_combined.reset_index(drop=True, inplace=True)
    return df_combined

#===================================================================================================

def main(args):

    # Change working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Command line arguments
    month = args.month
    year = args.year

    # Get current file path
    parent_path = os.path.dirname(os.path.abspath(__file__))
    date = year + '_' + month
    
    # Import CSV data from selected month and year
    df = extract_data(parent_path + '\\Statements',date)

    # Import categories and keywords from json files
    json_dir = os.path.join(parent_path,'ClassificationData')
    json_parser = JSON()
    json_parser.parse_files(json_dir)
    categories_keywords = json_parser.get_classification_dict()
    expenses_categories = json_parser.get_expense_categories()
    income_categories = json_parser.get_income_categories()

    # Sort transactions into their respective categories
    df['CATEGORY'] = df['DESCRIPTION'].apply(lambda x: group_transactions(x, categories_keywords))

    # Group all expenses and incomes in their respective dataframes
    df_expenses = df[df['CATEGORY'].isin(expenses_categories)]
    df_income = df[df['CATEGORY'].isin(income_categories)]

    # Calculate totals for expenses and income
    total_expenses = df_expenses['AMOUNT'].sum()
    total_income = df_income['AMOUNT'].sum()

    # Sort categories by most expensive
    categories_unsorted = []
    for category in sorted(df['CATEGORY'].unique()):
        grouped_transactions = df[df['CATEGORY'] == category]
        group_cost = grouped_transactions.values[:,1].sum()
        categories_unsorted.append([category,group_cost])
    categories_sorted = sorted(categories_unsorted, key=lambda x: x[1], reverse = False)

    # Create a DataFrame
    max_len = max(len(expenses_categories), len(income_categories))
    expenses_categories.extend([None] * (max_len - len(expenses_categories)))
    income_categories.extend([None] * (max_len - len(income_categories)))
    df_categories = pd.DataFrame({
        "Expenses": expenses_categories,
        "Income": income_categories
    })

    # Export data to csv
    file_path_sorted_transactions = os.path.join(parent_path,
                                                 'Outputs',
                                                 'Sorted_Transactions_' + date + '.csv')
    file_path_categories = os.path.join(parent_path,'Outputs','Categories.csv')
    df.to_csv(file_path_sorted_transactions, index=False)
    df_categories.to_csv(file_path_categories, index=False)

    # Command line output
    interface = Interface()
    if args.verbose:
        interface.print_sorted_transactions(args,
                                            df,
                                            categories_sorted,
                                            income_categories,
                                            expenses_categories,
                                            total_income,
                                            total_expenses)
    
    # Status message
    interface.print_status_message(file_path_sorted_transactions,
                                   file_path_categories)
    
#===================================================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort transactions for selected month and year.')
    parser.add_argument('--month', required=True, type=str, help='Selected month')
    parser.add_argument('--year', required=True, type=str, help='Selected year')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    args = parser.parse_args()

    main(args)