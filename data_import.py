import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
import glob
from tqdm import tqdm


class OregonProcess:
    
    def __init__(self):
        self.import_data_dask_flag = False
        self.oregon_only_flag = False        

    def _import_data_dask(self)-> None:
        """
        This function imports raw data from directory using dask and returns a dictionary of dask DataFrames.

        """
        input_dir = os.path.abspath("data\\*\\*")

        data_paths = glob.glob(input_dir, recursive=True)

        self.raw_data_dict = {}

        for data in tqdm(data_paths, desc="file import"):
            name = os.path.basename(data).split('.')[0]
            self.raw_data_dict[name] = dd.read_csv(data)
        self.import_data_dask_flag = True

        return None

    def _oregon_only(self):
        """
        This function trims input data to only contain data regarding Oregon counties.

        Details
        -------
        * Loops through tables in raw data dictionary.
        * Selects data from Oregon counties based on 'fips' numbers which have 41 as the first two digits based on values >41000 and <42000.
        * Converts dask DataFrames to pandas DataFrames.
        * Saves resulting pandas DataFrames to new dictionary.
        """
        assert self.import_data_dask_flag, "Please run _import_data_dask before _oregon_only."
        self.oregon_data_dict = {}
        for keyval in tqdm(self.raw_data_dict.keys(), desc='Selecting Oregonian rows'):
            table = self.raw_data_dict[keyval]
            table = table.loc[(table['fips']>41000) & (table['fips']<42000)].copy()
            table = table.compute()
            self.oregon_data_dict[keyval] = table
        
        self.oregon_only_flag = True
        return None
    
    def save_new_data(self):
        """
        This function saves the new DataFrames as csvs.
        
        """
        assert self.oregon_only_flag, "Please run oregon_only before save_new_data."

        os.makedirs('./processed_data', exist_ok=True)
        print('saving Oregon data into new csvs')

        for keyval in tqdm(self.oregon_data_dict.keys(), desc = 'table saving'):
            table = self.oregon_data_dict[keyval]
            table.to_csv(f'./processed_data/oregon_{keyval}.csv', index=False)
        print('Oregon data saved into csvs.')
        return None


    def oregon_data_runner(self):
        """
        This function runs the other functions of the class in the correct order.
        """

        self._import_data_dask()
        self._oregon_only()
        self.save_new_data()

        return self.oregon_data_dict

def oregon_import():
    """
    Imports Oregon tables from processed data folder. Also sets variable types for columns of resulting DataFrames.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    input_dir = os.path.abspath("processed_data\\*")

    data_paths = glob.glob(input_dir, recursive=True)

    oregon_data_dict = {}
    dtypes = {
        'fips': int,
        'date': str,
        'PRECTOT': float,
        'PS': float,
        'QV2M': float,
        'T2M': float,
        'T2MDEW': float,
        'T2MWET': float,
        'T2M_MAX': float,
        'T2M_MIN': float,
        'T2M_RANGE': float,
        'TS': float,
        'WS10M': float,
        'WS10M_MAX': float,
        'WS10M_MIN': float,
        'WS10M_RANGE': float,
        'WS50M': float,
        'WS50M_MAX': float,
        'WS50M_MIN': float,
        'WS50M_RANGE': float,
        'score': float
    }
    parse_dates = ['date']

    for data in tqdm(data_paths, desc="file import"):
        name = os.path.basename(data).split('.')[0]
        tablename = '_'.join(name.split('_')[1:])
        oregon_data_dict[tablename] = pd.read_csv(data, dtype = dtypes, parse_dates=parse_dates)

    return oregon_data_dict