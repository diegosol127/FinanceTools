# Import Python libraries
import os
import json
import pandas as pd

# CSV transaction parser class
class CSV:

    # Constructor
    def __init__(self) -> None:
        pass
    
    # Return a data parser based on the name of the institution
    def parse_file(self, file_path: str) -> pd.DataFrame:
        parsers = {
            'AmericanExpress': self.parse_AmericanExpress,
            'Optum': self.parse_Optum,
            'WellsFargo': self.parse_WellsFargo,
            'SoFi': self.parse_SoFi
        }

        institution = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        if institution in parsers:
            return parsers[institution](file_path)
        else:
            raise ValueError(f"No parser available for institution: {institution}")
    
    # Parse CSV files in the format given by American Express
    def parse_AmericanExpress(self, file_path) -> pd.DataFrame:
        df = pd.read_csv(file_path, header=None)
        df.drop(0, axis=0, inplace=True)
        df = df[df.columns[[0,2,1]]]
        df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
        df['AMOUNT'] = -df['AMOUNT'].astype(float)
        df['INSTITUTION'] = 'AmericanExpress'
        return df

    # Parse CSV files in the format given by Optum
    def parse_Optum(self, file_path) -> pd.DataFrame:
        df = pd.read_csv(file_path, header=None)
        df.drop(0, axis=0, inplace=True)
        df.drop(3, axis=1, inplace=True)
        df = df[df.columns[[0,2,1]]]
        df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
        df['AMOUNT'] = df['AMOUNT'].str.strip('$').astype(float)
        df['INSTITUTION'] = 'Optum'
        return df

    # Parse CSV files in the format given by SoFi
    def parse_SoFi(self, file_path) -> pd.DataFrame:
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

    # Parse CSV files in the format given by Wells Fargo
    def parse_WellsFargo(self, file_path) -> pd.DataFrame:
        df = pd.read_csv(file_path, header=None)
        df.drop([2,3],axis=1, inplace=True)
        df.rename(columns={0: 'DATE', 1: 'AMOUNT', 4: 'DESCRIPTION'}, inplace=True)
        df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(',','')
        df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
        df['INSTITUTION'] = 'Wells Fargo'
        return df
    
# JSON classification parser class
class JSON:

    # Constructor
    def __init__(self) -> None:
        self.classification_dict = {}
        self.expenses_list = []
        self.income_list = []

    # Get a list of all JSON files in a given directory
    def parse_files(self, directory: str) -> None:
        all_files = os.listdir(directory)
        json_files = [file for file in all_files if file.endswith('.json')]
        for json_file in json_files:
            file_path = os.path.join(directory, json_file)
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.classification_dict.update(data)
                if 'expenses' in json_file:
                    self.expenses_list.append(list(data.keys())[0])
                else:
                    self.income_list.append(list(data.keys())[0])

    # Get classification dictionary
    def get_classification_dict(self) -> list:
        return self.classification_dict

    # Get list of expense categories
    def get_income_categories(self) -> list:
        return self.expenses_list

    # Get list of income categories
    def get_expense_categories(self) -> list:
        return self.income_list
