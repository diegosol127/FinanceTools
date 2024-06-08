# Import libraries
import os
import json
import sys
import numpy as np
import pandas as pd


def parse_Optum(file_path):
    # Parse CSV files in the format given by Optume
    df = pd.read_csv(file_path, header=None)
    df.drop(0, axis=0, inplace=True)
    df.drop(3, axis=1, inplace=True)
    df = df[df.columns[[0,2,1]]]
    df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
    df['AMOUNT'] = df['AMOUNT'].str.strip('$').astype(float) 
    df['INSTITUTION'] = 'Optum'
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
    
def get_institution_name(path):
    # Extract the institution name from the folder path
    return os.path.basename(os.path.dirname(path))

def parse_file(file_path):
    # Return a data parser based on the name of the institution
    parsers = {
        'Optum': parse_Optum,
        'WellsFargo': parse_WellsFargo
    }

    institution = get_institution_name(file_path)
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
def main():
    # Change working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Command line arguments
    if '-v' in sys.argv or '--verbose' in sys.argv:
        verbose = True
    else:
        verbose = False

    # User input
    month = input('Enter Month (mm): ')
    year = input('Enter Year (yyyy): ')

    # Import categories and keywords from json files
    categories_keywords = {}
    json_dir = 'ClassificationData'
    json_ext = '.json'
    # TASK: automate this step by reading the names of the json files
    json_files = [
        '_income',
        'car',
        'gas',
        'groceries',
        'loans',
        'medical',
        'memberships',
        'personal',
        'rent',
        'restaurants',
        'travel',
    ]

    for json_file in json_files:
        with open(os.path.join(json_dir,json_file+json_ext), 'r') as file:
            category_data = json.load(file)
            categories_keywords.update(category_data)

    # Import data from csv files
    parent_path = os.path.dirname(os.path.abspath(__file__))
    date = year + '_' + month

    # Function to categorize transactions in dataframe
    def group_transactions(description):
        for category, keywords in categories_keywords.items():
            for keyword in keywords:
                if keyword.upper() in description.upper():
                    return category
        return '***Unlabelled***'
    
    df = extract_data(parent_path + '\\Statements',date)

    # Sort transactions into their respective categories
    df = df.copy()
    df['CATEGORY'] = df['DESCRIPTION'].apply(group_transactions)
    df.reindex(columns=['DATE', 'AMOUNT', 'DESCRIPTION', 'INSTITUTION', 'CATEGORY'])
    df_expenses = df[df['CATEGORY'] != 'Income']
    df_income = df[df['CATEGORY'] == 'Income']
    total_expenses = df_expenses.values[:,1].sum()
    total_income = df_income.values[:,1].sum()

    # Sort categories by most expensive
    categories_unsorted = []
    for category in sorted(df['CATEGORY'].unique()):
        grouped_transactions = df[df['CATEGORY'] == category]
        group_cost = grouped_transactions.values[:,1].sum()
        categories_unsorted.append([category,group_cost])
    categories_sorted = sorted(categories_unsorted, key=lambda x: x[1], reverse = False)

    # Export data to csv
    file_path_export_csv = os.path.join(parent_path,'Outputs','Sorted_Transactions_' + date + '.csv')
    df.to_csv(file_path_export_csv, index=False)

    if verbose:
        split_1 = '***************************************************'
        split_2 = '---------------------------------------------------'
        split_3 = '==================================================='
        print(f'\n\n\n{split_1*3}\n{split_2*3}\nSTATEMENT ANALYSIS: {year}-{month}\n{split_2*3}\n{split_1*3}\n')
        for category, group_cost in categories_sorted:
            grouped_transactions = df[df['CATEGORY'] == category]
            if category != 'Income':
                print(f'''\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   |   
                      {group_cost/total_expenses*100:0.2f}% Total Costs   \n{split_2*3}''')
            else:
                print(f'\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   \n{split_2*3}')
            print(grouped_transactions.iloc[:,:4].to_string(index=False,max_colwidth=114,justify='justify-all',col_space=[15,15,100,20]))

        # Print net gain/loss for time period
        net_gain = df.values[:,1].sum()
        print(f'\n\n\n\n\n{split_2*3}\nTotal Expenses for {year}-{month}: ${total_expenses:0.2f}\n{split_2*3}')
        print(f'Total Income for {year}-{month}:   ${total_income:0.2f}\n{split_2*3}')
        print(f'\n\n\n\n\n{split_3*3}\nNet Gain/Loss for {year}-{month}:  ${net_gain:0.2f}\n{split_3*3}\n')

    # Status message
    print(f'\nSuccess! Transactions have been sorted to\n{file_path_export_csv}\n\n')

if __name__ == '__main__':
    main()