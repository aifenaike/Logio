try:
    import pandas as pd
    from pandas import DataFrame
    import numpy as np
    import scipy.stats as stats
    from typing import Union, Any, List
    import os
    import json
    import lasio
    from collections import defaultdict

except ImportError:
    print("Install the libraries before importing")

class DataNotFoundException(Exception):
    """Data not found"""
    pass

class InvalidFormatException(Exception):
    """Format does not conform with the required format"""
    pass

class Analysis:
    """"
    This class reads and performs basic data analysis.
    It houses five methods with their functionalities bordering on:
    
       | reading of files {csv, xlsx, json, las};
       | returning a statistical description of the file;
       | returning a correlation matrix of the numerical features;
       | returning a cross tab of categorical features specified;
       | returning a frequency table of categorical features specified.
         
    """
    
    def __init__(self):
        "No global attribute to initialize."
        
    def read_file(self, filename: str) -> pd.DataFrame:
        """
            reads in file in different supported formats into a DataFrame

            params:

                `filename -> the name of the file to read`

            returns:
                A dataframe
        """
        formats = [
            "xlsx",
            "csv",
            "las",
            "json"
        ]
        if filename.split(".")[-1].lower() not in formats:
            raise InvalidFormatException(f"File {filename} not in the allowed format")

        cur_path = os.getcwd()
        full_path = cur_path + "/" + filename
        if filename.endswith(".LAS") or filename.endswith(".las"):
            data = lasio.read(full_path).df()
            data = data.reset_index()
            return data
        if filename.endswith(".json"):
            data = pd.read_json(filename)
        elif filename.endswith(".csv"):
            data = pd.read_csv(filename)
        elif filename.endswith(".xlsx"):
            data = pd.read_excel(filename)
        
        return data
    
    def describe(self, data):
        '''
         this function returns the mean,median,min,max,skewness,kurtosis and Jarque Bera of numerical columns of a dataset.\n
         Note:
         -------\n
         Jarque Bera test will return NaN for columns with missing values
    
         Parameters:
         ------------\n
         data: The dataset to be analysed in csv,xlsx or las format.\n
         Returns:
         ---------\n
         returns the mean,median,min,max,skewness,kurtosis and Jarque Bera summary of a dataset.
         '''
        #specifying the datatype == number
        df = data.select_dtypes(include="number")
        #creating a dictionary of the data description
        df_mean = df.mean().to_dict()
        df_median = df.median().to_dict()
        df_std = df.std().to_dict()
        df_min = df.min().to_dict()
        df_max = df.max().to_dict()
        df_skew = df.skew().to_dict()
        df_kurt = df.kurtosis().to_dict()
        df_jarque = {}
        for key in df.columns:
            result = stats.jarque_bera(df[key])
            df_jarque[key] = result.statistic
        #creating a dataframe that will be render witht the description of our data
        describe = pd.DataFrame([
               list(df_mean.values()),
               list(df_median.values()),
               list(df_std.values()),
               list(df_min.values()),
               list(df_max.values()),
               list(df_skew.values()),
               list(df_kurt.values()),
               list(df_jarque.values())],columns=list(df_mean.keys()),\
            index=['mean','median','std','min','max','skewness','kurtosis','Jarque_bera'])
        #returning the dataframe
        return describe
    
    def correlate(self, df : DataFrame, method : str = 'pearson'):
        """
        Compute pairwise correlation of columns, excluding NA/null 
        and non-numerical values.
    
        Parameters
        ----------
        method : {'pearson', 'kendall', 'spearman'}
            Method of correlation:

            * pearson : standard correlation coefficient
            * kendall : Kendall Tau correlation coefficient
            * spearman : Spearman rank correlation

        Returns
        -------
        DataFrame
            Correlation matrix.
            Calculates the pairwise correlation between columns in a dataframe
        """

        # Coerce the input into a dataframe if it is not one already
        df = DataFrame(df) 

        # Drop NA values from the dataframe
        df.dropna(inplace = True) 
    
        # Selects the numerical columns in the dataframe
        new_df = df.select_dtypes(include = 'number') 
    
        return new_df.corr(method = method)
    
    def cross_tab(self, data, row, column):
        """
        returns a crosstab for only two selected categorical feature in the dataset.\n
       
        Parameters:
        ----------\n
           data : Dataset in csv,xlsx, json or las format.
                 The dataset to extract the crosstab of the selected categorical features (columns)\n
           row :     The first selected categorical features(column)\n
           column:   The second selected categorical feature(column)
       
   
        Returns:
        -------\n
          return a crosstab for  two selected categorical feature in the dataset.\n

        """
        #a sub function to use pandas crosstab under the hood
        def create_crosstab(data,row,column):
            tab = pd.crosstab(data[row],data[column]) 
            cat_col = [col for col in data.columns if (data[col].dtype != 'int64' and data[col].dtype !='float64')]
            if (row in cat_col and column in cat_col):
                return tab
            elif (row not in cat_col or column not in cat_col):
                raise TypeError ('Unsupported column type, Input a column with categorical variables')
    
        #called the subfunction
        crosstab = create_crosstab(data=data,row=row,column=column)
        return crosstab

    def frequencyTable(self, data: Union[pd.DataFrame, pd.Series, Any], 
                   col_names: Union[str, List[str]]) -> Union[pd.DataFrame,List[pd.DataFrame]]:
        """
            Computes a frequency table for the categorical variables in the dataframe.

            params:

                `data -> pandas dataframe that the frequency table is computed from.`

                `col_names -> a string or a list of strings indicating the columns that
                             contains the categorical data`

            returns:

                a pandas dataframe that contains the frequency table.
        """
        if data is None or col_names is None:
            raise DataNotFoundException("No data was provided or no column names was provided")

        if isinstance(col_names, str):
            if data[col_names].dtype != np.dtype("object"):
                raise InvalidFormatException("The column specified is not a categorical column")

            target = data[col_names]
            try:
                target.isnull().sum() == 0
                uniques = sorted(target.unique())
            except TypeError:
                print('Missing values detected in one or both of the columns selected')
                print('The frequency and percentage of the missing value will not be accounted for')
            uniques = target.unique()
            frequencies = defaultdict(list)
            for val in uniques:
                for value in target.values:
                    if val == value:
                        frequencies[val].append(1)
                count = sum(i for i in frequencies[val])
                frequencies[val] = count
                    
                
        
            names = [i[0] for i in list(frequencies.items())]
            values = [i[1] for i in list(frequencies.items())]
            freq = [v / sum(values) * 100 for v in values]
            return pd.DataFrame({'frequencies': values, "percentage":freq}, index=[names])
        else:
            temp = []
            for col in col_names:
                if data[col].dtype != np.dtype("object"):
                    raise InvalidFormatException("The column specified is not a categorical column")

                target = data[col]
                try:
                    target.isnull().sum() == 0
                    uniques = sorted(target.unique())
                except TypeError:
                    print('Missing values detected in one or both of the columns selected')
                    print('The frequency and percentage of the missing value will not be accounted for')
                uniques = target.unique()
                frequencies = defaultdict(list)
                for val in uniques:
                    for value in target.values:
                        if val == value:
                            frequencies[val].append(1)
                    count = sum(i for i in frequencies[val])
                    frequencies[val] = count
                    
                
        
                names = [i[0] for i in list(frequencies.items())]
                values = [i[1] for i in list(frequencies.items())]
                freq = [v / sum(values) * 100 for v in values]
                temp.append(pd.DataFrame({'frequencies': values, "percentage":freq}, index=[names]))
            return temp
        
        
class FileConverter():
    """
    This class converts files from one format to another.
    The allowed extensions are tailored towards possible well-log data formats:
        |csv, 
        |xlsx, 
        |json
        |las
    """
    
    def __init__(self, filename, output_format):
        "Initialize filename and output_format attribute."
        
        self.filename = filename
        self.output_format = output_format
    
    def convert_file(self):
        """
        This method takes in a data format, and returns the data
        in a format specified by the user, in the current working directory.
        
        param_definition
        ---------------
        input_format :  the input file format.
        output_format : the specified output file format ('csv, xlsx, json, las')
    
        The csv format is the central format:
        for any conversion from an input_format to an output_format other than csv,
        the input_format is first converted to a csv, and afterwards, converted to the required output file format.
    
        """
        ALLOWED_EXTENSIONS = {"csv", "xlsx", "json", "las"}
    
        print(f'The allowed file extensions are {ALLOWED_EXTENSIONS}')
        output_format = str.lower(self.output_format)
    
        print('\nThe data to be read has to be in the current working directory')
        filename = self.filename
        
         # The following methods seek to convert files from csv to the specified output format
    
        def csv_to_xlsx(self):
            """converts from csv to xlsx"""
        
            df = pd.read_csv(self.filename)
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.xlsx"
            df.to_excel(fn, index=False)
            return fn
   
        def csv_to_json(self):
            """converts from csv to json"""
        
            df = pd.read_csv(self.filename)
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.json"
            df.to_json(fn)
            return fn
    
        def csv_to_las(self):
            """converts from csv to las"""
        
            df = pd.read_csv(self.filename)
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.las"
            las_file = lasio.LASFile()
            for col in df.columns:
                las_file.add_curve(col, df[col])
            las_file.write(fn)
            return fn
    
        def csv_checker(self, df, fn):
            """
            the csv format is the central converting format, and this method seeks to address 
            duplication of csv format, ensuring that the csv format file is saved in the working directory
            only when the output format specified is csv.
    
            """
        
            if self.output_format == "csv":
                df.to_csv(fn, index=False)
            else:
                pass 

        # The following functions seek to convert from other file types to csv format.
    
        def xlsx_to_csv(self):
            """converts excel to csv"""
        
            df = pd.read_excel(self.filename)
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.csv"
            csv_checker(self, df, fn)
            return fn
    
        def json_to_csv(self):
            """converts json to csv"""
            
            df = pd.read_json(self.filename)
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.csv"
            csv_checker(self, df, fn)
            return fn
    
        def las_to_csv(self):
            """converts las to csv"""
        
            data = lasio.read(self.filename)
            df = data.df()
            df = df.reset_index()
            filename = str.lower(self.filename)
            fn = f"{filename.rsplit('.')[0]}.csv"
            csv_checker(self, df, fn)
            return fn
    
        start_time = time.time()
        if (str.lower(filename.rsplit('.')[1]) in ALLOWED_EXTENSIONS
            and output_format in ALLOWED_EXTENSIONS):
        
            input_format = str.lower(filename.rsplit('.')[1])
            if input_format == 'csv':
                if output_format == 'csv':
                    print('\nError: same input and output format specified.')
                elif output_format == 'xlsx':
                    fn = csv_to_xlsx(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'json':
                    fn = csv_to_json(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'las':
                    fn = csv_to_las(self)
                    print('\nDone. The output data has been saved in the current working directory')
                
            elif input_format == 'xlsx':
                if output_format == 'xlsx':
                    print('\nError: same input and output format specified')
                elif output_format == 'csv':
                    fn = xlsx_to_csv(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'json':
                    new_fn = xlsx_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_json(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'las':
                    new_fn = xlsx_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_las(self)
                    print('\nDone. The output data has been saved in the current working directory')
                
            elif input_format == 'json':
                if output_format == 'json':
                    print('\nError: same input and output format specified')
                elif output_format == 'csv':
                    fn = json_to_csv(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'xlsx':
                    new_fn = json_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_xlsx(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'las':
                    new_fn = json_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_las(self)
                    print('\nDone. The output data has been saved in the current working directory')
                
            elif input_format == 'las':
                if output_format == 'las':
                    print('\nError: same input and output format specified')
                elif output_format == 'csv':
                    fn = las_to_csv(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'json':
                    new_fn = las_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_json(self)
                    print('\nDone. The output data has been saved in the current working directory')
                elif output_format == 'xlsx':
                    new_fn = las_to_csv(self)
                    self.filename = new_fn
                    fn = csv_to_xlsx(new_fn, output_format)
                    print('\nDone. The output data has been saved in the current working directory')
    
        else:
            print("\nError: Unsupported file format. Check your input and output file format")
        end_time = time.time()
        time_lapsed = end_time-start_time
        print(f"\n {time_lapsed} seconds")