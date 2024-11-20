# Import Python libraries
import argparse
import pandas as pd

class Interface:
    def __init__(self) -> None:
        pass
    
    def print_sorted_transactions(self,
                                  mainArgs: argparse.Namespace,
                                  df: pd.DataFrame,
                                  categories_sorted: list,
                                  income_categories: list,
                                  expenses_categories: list,
                                  total_income: float,
                                  total_expenses: float
                                  ) -> None:
        month = mainArgs.month
        year = mainArgs.year
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
        net_gain = total_income + total_expenses
        print(f'\n\n\n\n\n{split_2*3}\nTotal Expenses for {year}-{month}: ${total_expenses:0.2f}\n{split_2*3}')
        print(f'Total Income for {year}-{month}:   ${total_income:0.2f}\n{split_2*3}')
        print(f'\n\n\n\n\n{split_3*3}\nNet Gain/Loss for {year}-{month}:  ${net_gain:0.2f}\n{split_3*3}\n')

    def print_status_message(self,
                             file_path_sorted_transactions: str,
                             file_path_categories: str
                             ) -> None:
        print('\n\nSuccess!')
        print(f'\nTransactions have been sorted to\n\t{file_path_sorted_transactions}')
        print(f'\nCategories have been sorted to\n\t{file_path_categories}\n\n')

