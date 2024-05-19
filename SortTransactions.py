# Import libraries
import os
import json
import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    # Command line arguments
    if "-verbose" in sys.argv:
        verbose = True
    else:
        verbose = False

    # Bank options: WellsFargo, Optum
    # Account options: Checking, Savings, Credit, HSA
    bank = "MainBank"
    accounts = ["Checking", "Savings", "Credit"]
    month = input('Enter Month (mm): ')
    year = input('Enter Year (yyyy): ')

    # Change working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Import categories and keywords from json files
    categories_keywords = {}
    json_dir = "ClassificationData"
    json_ext = ".json"
    # TASK: automate this step by reading the names of the json files
    json_files = [
        "_income",
        "car",
        "gas",
        "groceries",
        "loans",
        "medical",
        "memberships",
        "personal",
        "rent",
        "restaurants",
        "travel",
    ]

    for json_file in json_files:
        with open(os.path.join(json_dir,json_file+json_ext), 'r') as file:
            category_data = json.load(file)
            categories_keywords.update(category_data)

    # Import data from csv files
    parent_path = os.path.dirname(os.path.abspath(__file__))
    date = year + "_" + month
    df_list = []
    for account in accounts:
        file_path_import = os.path.join(parent_path,"Statements",bank + "_" + account + "_" + date + ".csv")
        df_list.append(pd.read_csv(file_path_import,header=None))

    # Function to categorize transactions in dataframe
    def group_transactions(description):
        for category, keywords in categories_keywords.items():
            for keyword in keywords:
                if keyword.upper() in description.upper():
                    return category
        return "***Unlabelled***"

    # Create and format the dataframe
    df = pd.concat(df_list,ignore_index=True)
    if bank == "MainBank":
        df = df.drop([2,3],axis=1)
        df[4] = df[4].str.replace(',','')
    else:
        df = df.drop(0,axis=0)
        df = df.drop(3,axis=1)
        df = df[df.columns[[0,2,1]]]
        df_list = df.values[:,1].tolist()
        df_list = [s.strip('$') for s in df_list]
        df_list = list(map(float,df_list))
        df.values[:,1] = np.asarray(df_list)
        
    column_names = ["DATE","AMOUNT","DESCRIPTION"]
    df.columns = column_names
    df = df.sort_values(by="DATE",ascending=True).reset_index(drop=True)

    # Sort transactions into their respective categories
    df = df.copy()
    df["CATEGORY"] = df["DESCRIPTION"].apply(group_transactions)
    df_expenses = df[df["CATEGORY"] != "Income"]
    df_income = df[df["CATEGORY"] == "Income"]
    total_expenses = df_expenses.values[:,1].sum()
    total_income = df_income.values[:,1].sum()

    # Sort categories by most expensive
    categories_unsorted = []
    for category in sorted(df["CATEGORY"].unique()):
        grouped_transactions = df[df["CATEGORY"] == category]
        group_cost = grouped_transactions.values[:,1].sum()
        categories_unsorted.append([category,group_cost])
    categories_sorted = sorted(categories_unsorted, key=lambda x: x[1], reverse = False)

    # Export data to csv
    account_str = accounts[0]
    if len(accounts) > 1:
        for i in range(1,len(accounts)):
            account_str += "_" + accounts[i]
    file_path_export_csv = os.path.join(parent_path,"Outputs",bank + "_" + account_str + "_" + date + "_sorted.csv")
    df.to_csv(file_path_export_csv, index=False)

    if verbose:
        # Print outputs by category
        # file_path_export_txt = os.path.join(parent_path,"Outputs",bank + "_" + account_str + "_" + date + "_sorted.txt")
        # if os.path.isfile(file_path_export_txt):
        #     os.remove(file_path_export_txt)
        # f = open(file_path_export_txt, "a")
        # f.close()
        split_1 = '********************************************'
        split_2 = '--------------------------------------------'
        split_3 = '============================================'
        print(f'\n\n\n{split_1*3}\n{split_2*3}\nSTATEMENT ANALYSIS: {bank} // {accounts} // {year}-{month}\n{split_2*3}\n{split_1*3}\n\n')
        for category, group_cost in categories_sorted:
            grouped_transactions = df[df["CATEGORY"] == category]
            if category != "Income":
                print(f'\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   |   {group_cost/total_expenses*100:0.2f}% Total Costs   \n{split_2*3}')
            else:
                print(f'\n\n\n{split_3*3}\n{category}:   ${group_cost:0.2f}   \n{split_2*3}')
            print(grouped_transactions.iloc[:,:3].to_string(index=False,max_colwidth=114,justify='justify-all',col_space=[15,15,100]))

        # Print net gain/loss for time period
        net_gain = df.values[:,1].sum()
        print(f"\n\n\n\n\n{split_2*3}\nTotal Expenses for {year}-{month}: ${total_expenses:0.2f}\n{split_2*3}")
        print(f"Total Income for {year}-{month}:   ${total_income:0.2f}\n{split_2*3}")
        print(f"\n\n\n\n\n{split_3*3}\nNet Gain/Loss for {year}-{month}:  ${net_gain:0.2f}\n{split_3*3}\n")

    # Status message
    print(f"\nSuccess! Transactions have been sorted to\n{file_path_export_csv}\n\n")
