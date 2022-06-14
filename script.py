try:
    import pandas as pd
    import numpy as np
    from typing import Union, Any, List
    import os
    import json
    import lasio
except ImportError:
    print("Import the libraries before importing")

class DataNotFoundException(Exception):
    """Data not found"""
    pass

class InvalidFormatException(Exception):
    """Format does not conform with the required format"""
    pass

def frequencyTable(data: Union[pd.DataFrame, pd.Series, Any], col_names: Union[str, List[str]]) -> Union[pd.DataFrame,List[pd.DataFrame]]:
    """
        Computes a frequency table for the categorical variables in the dataframe.

        params:

            `data -> pandas dataframe that the frequency table is computed from.`

            `col_names -> a string or a list of strings indicating the columns that contains the categorical data`

        returns:

            a pandas dataframe that contains the frequency table.
    """
    if data is None or col_names is None:
        raise DataNotFoundException("No data was provided or no column names was provided")

    if isinstance(col_names, str):
        if data[col_names].dtype != np.dtype("Object"):
            raise InvalidFormatException("The column specified is not a categorical column")

        target = data[col_names]
        uniques = sorted(target.unique())
        frequencies = {}
        for val in uniques:
            for value in target.values:
                if val == value:
                    frequencies[val] += 1
                else:
                    frequencies[val] += 0
        
        names, values = frequencies.items()
        freq = [v / sum(values) * 100 for v in values]
        return pd.DataFrame(data=[names, values, freq], columns=["Nmaes", "Frequency", "Percentage"])
    else:
        temp = []
        for col in col_names:
            if data[col].dtype != np.dtype("Object"):
                raise InvalidFormatException("The column specified is not a categorical column")

            target = data[col]
            uniques = sorted(target.unique())
            frequencies = {}
            for val in uniques:
                for value in target.values:
                    if val == value:
                        frequencies[val] += 1
                    else:
                        frequencies[val] += 0
            
            names, values = frequencies.items()
            freq = [v / sum(values) * 100 for v in values]
            temp.append(pd.DataFrame(data=[names, values, freq], columns=["Nmaes", "Frequency", "Percentage"]))
        return temp




def read(filename: str) -> pd.DataFrame:
    """
        reads in file in different supported formats into a DataFrame

        params:

            `filename -> the name of the file to read`

        returns:
            A dataframe
    """
    formats = [
        "xlsx",
        "xls",
        "csv",
        "segy",
        "las",
        "json"
    ]
    if filename.split(".")[-1].lower() not in formats:
        raise InvalidFormatException(f"File {filename} not in the right format")

    cur_path = os.getcwd()
    full_path = cur_path + "/" + filename
    if "LAS" in filename:
        data = lasio.read(full_path).df()
        return data
    else:
        return None