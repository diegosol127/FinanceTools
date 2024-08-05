# Import libraries
import argparse
import json
import os
import sys
import numpy as np
import pandas as pd

def get_classification_info(directory):
    # Get a list of all JSON files in a given directory
    classification_dict = {}
    expenses_list = []
    income_list = []
    all_files = os.listdir(directory)
    json_files = [file for file in all_files if file.endswith('.json')]
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            classification_dict.update(data)
            if 'expenses' in json_file:
                expenses_list.append(list(data.keys())[0])
            else:
                income_list.append(list(data.keys())[0])

    return classification_dict, expenses_list, income_list

def group_transactions(description, classification_dict):
    # Identify a category for the given transaction
    for category, keywords in classification_dict.items():
        for keyword in keywords:
            if keyword.upper() in description.upper():
                return category
    return '***Unlabelled***'

def parse_AmericanExpress(file_path):
    # Parse CSV files in the format given by American Express
    df = pd.read_csv(file_path, header=None)
    df.drop(0, axis=0, inplace=True)
    df = df[df.columns[[0,2,1]]]
    df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
    df['AMOUNT'] = -df['AMOUNT'].astype(float)
    df['INSTITUTION'] = 'AmericanExpress'
    return df

def parse_Optum(file_path):
    # Parse CSV files in the format given by Optum
    df = pd.read_csv(file_path, header=None)
    df.drop(0, axis=0, inplace=True)
    df.drop(3, axis=1, inplace=True)
    df = df[df.columns[[0,2,1]]]
    df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
    df['AMOUNT'] = df['AMOUNT'].str.strip('$').astype(float)
    df['INSTITUTION'] = 'Optum'
    return df

def parse_SoFi(file_path):
    # Parse CSV files in the format given by SoFi
    df = pd.read_csv(file_path, header=None)
    df.drop(0, axis=0, inplace=True)
    df.drop(2, axis=1, inplace=True)
    df.drop(4, axis=1, inplace=True)
    df.drop(5, axis=1, inplace=True)
    df = df[df.columns[[0,2,1]]]
    df.rename(columns={0: 'DATE', 3: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
    df['AMOUNT'] = df['AMOUNT'].astype(float)
    df['INSTITUTION'] = 'SoFi'
    return df

def parse_WellsFargo(file_path):
    # Parse CSV files in the format given by Wells Fargo
    df = pd.read_csv(file_path, header=None)
    df.drop([2,3],axis=1, inplace=True)
    df.rename(columns={0: 'DATE', 1: 'AMOUNT', 4: 'DESCRIPTION'}, inplace=True)
    df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(',','')
    df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    df['INSTITUTION'] = 'Wells Fargo'
    return df
    
def parse_file(file_path):
    # Return a data parser based on the name of the institution
    parsers = {
        'AmericanExpress': parse_AmericanExpress,
        'Optum': parse_Optum,
        'WellsFargo': parse_WellsFargo,
        'SoFi': parse_SoFi
    }

    institution = os.path.basename(os.path.dirname(file_path))
    if institution in parsers:
        return parsers[institution](file_path)
    else:
        raise ValueError(f"No parser available for institution: {institution}")
    
def extract_data(directory,date):
    # Extract the csv data from the selected directory
    df_combined = pd.DataFrame()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if date in file:
                file_path = os.path.join(root, file)
                try:
                    df = parse_file(file_path)
                    df_combined = pd.concat([df_combined,df],axis=0, ignore_index=True)
                    print(f"Processed {file_path}")
                except ValueError as e:
                    print(e)

    df_combined.sort_values(by='DATE', inplace=True)
    df_combined.reset_index(drop=True, inplace=True)
    return df_combined

#=================================================================================================
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
    categories_keywords, expenses_categories, income_categories = get_classification_info(json_dir)

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
    file_path_sorted_transactions = os.path.join(parent_path,'Outputs','Sorted_Transactions_' + date + '.csv')
    file_path_categories = os.path.join(parent_path,'Outputs','Categories.csv')
    df.to_csv(file_path_sorted_transactions, index=False)
    df_categories.to_csv(file_path_categories, index=False)

    # Command line output
    if args.verbose:
        split_1 = '***************************************************'
        split_2 = '---------------------------------------------------'
        split_3 = '==================================================='
        print(f'\n\n\n{split_1*3}\n{split_2*3}\nSTATEMENT ANALYSIS: {year}-{month}\n{split_2*3}\n{split_1*3}\n')
        for category, group_cost in categories_sorted:
            grouped_transactions = df[df['CATEGORY'] == category]
            if category in expenses_categories:
                print(f'''\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   |   {group_cost/total_expenses*100:0.2f}% Total Expenses   \n{split_2*3}''')
            elif category in income_categories:
                print(f'\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   |   {group_cost/total_income*100:0.2f}% Total Income   \n{split_2*3}')
            else:
                print(f'\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   \n{split_2*3}')
            category_spaces = [15,15,100,20]
            print(grouped_transactions.iloc[:,:4].to_string(index=False,max_colwidth=max(category_spaces),justify='justify-all',col_space=category_spaces))

        # Print net gain/loss for time period
        net_gain = df.values[:,1].sum()
        print(f'\n\n\n\n\n{split_2*3}\nTotal Expenses for {year}-{month}: ${total_expenses:0.2f}\n{split_2*3}')
        print(f'Total Income for {year}-{month}:   ${total_income:0.2f}\n{split_2*3}')
        print(f'\n\n\n\n\n{split_3*3}\nNet Gain/Loss for {year}-{month}:  ${net_gain:0.2f}\n{split_3*3}\n')

    # Status message
    print('\n\nSuccess!')
    print(f'\nTransactions have been sorted to\n\t{file_path_sorted_transactions}')
    print(f'\nCategories have been sorted to\n\t{file_path_categories}\n\n')

#==================================================================================================================================================================================================
#==================================================================================================================================================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort transactions for selected month and year.')
    parser.add_argument('--month', required=True, type=str, help='Selected month')
    parser.add_argument('--year', required=True, type=str, help='Selected year')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    args = parser.parse_args()

    main(args)