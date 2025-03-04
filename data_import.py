import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
import glob
from tqdm import tqdm


class OregonImport:
    
    def __init__(self):
        self.import_data_dask_flag = False
        self.oregon_only_flag = False        

    def _import_data_dask(self)-> None:
        """
        This function imports raw data from directory using dask and returns a dictionary of dask DataFrames.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
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

        Parameters
        ----------
        None
        """
        assert self.import_data_dask_flag, "Please run _import_data_dask before _oregon_only."
        self.oregon_data_dict = {}
        for keyval in tqdm(self.raw_data_dict.keys(), desc='table management'):
            table = self.raw_data_dict[keyval]
            table = table.loc[(table['fips']>41000) & (table['fips']<42000)].copy()
            table = table.compute()
            self.oregon_data_dict[keyval] = table
        
        self.oregon_only_flag = True
        return None
    
    def save_new_data(self):
        """
        This function saves the new DataFrames as csvs"""
        assert self.oregon_only_flag, "Please run oregon_only before save_new_data."

        os.makedirs('./processed', exist_ok=True)
        print('saving oregon data into new csvs')

        for keyval in tqdm(self.oregon_data_dict.keys(), desc = 'table saving'):
            table = self.oregon_data_dict[keyval]
            table.to_csv(f'/processed/oregon_{table}.csv')
        print('new oregon data saved into csvs.')
        return None


    def oregon_data_runner(self):
        """
        This function runs the other functions of the class in the correct order.
        """

        self._import_data_dask()
        self.save_new_data()
        self._oregon_only()

        return self.oregon_data_dict