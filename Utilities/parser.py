# Import Python libraries
import os
import pandas as pd

# Transaction parser class
class Parser:
    def __init__(self) -> None:
        pass
    
    def parse_file(self, file_path: str) -> pd.DataFrame:
        # Return a data parser based on the name of the institution
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
    
    def parse_AmericanExpress(self, file_path):
        # Parse CSV files in the format given by American Express
        df = pd.read_csv(file_path, header=None)
        df.drop(0, axis=0, inplace=True)
        df = df[df.columns[[0,2,1]]]
        df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
        df['AMOUNT'] = -df['AMOUNT'].astype(float)
        df['INSTITUTION'] = 'AmericanExpress'
        return df

    def parse_Optum(self, file_path):
        # Parse CSV files in the format given by Optum
        df = pd.read_csv(file_path, header=None)
        df.drop(0, axis=0, inplace=True)
        df.drop(3, axis=1, inplace=True)
        df = df[df.columns[[0,2,1]]]
        df.rename(columns={0: 'DATE', 2: 'AMOUNT', 1: 'DESCRIPTION'}, inplace=True)
        df['AMOUNT'] = df['AMOUNT'].str.strip('$').astype(float)
        df['INSTITUTION'] = 'Optum'
        return df

    def parse_SoFi(self, file_path):
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

    def parse_WellsFargo(self, file_path):
        # Parse CSV files in the format given by Wells Fargo
        df = pd.read_csv(file_path, header=None)
        df.drop([2,3],axis=1, inplace=True)
        df.rename(columns={0: 'DATE', 1: 'AMOUNT', 4: 'DESCRIPTION'}, inplace=True)
        df['DESCRIPTION'] = df['DESCRIPTION'].str.replace(',','')
        df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
        df['INSTITUTION'] = 'Wells Fargo'
        return df