#imported the necessary libraries 
import pandas as pd 
import scipy.stats as stats

#Crosstab Function
def cross_tab(data,row,column):
    """
    returns a crosstab for only two selected categorical feature in the dataset.\n
   
    Parameters:
    ----------\n
       data : Dataset in csv,xlsx or las format.
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

    
#Descriptive Function
def descriptive(data):
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
               list(df_jarque.values())],columns=list(df_mean.keys()),index=['mean','median','std','min','max','skewness','kurtosis','Jarque_bera'])
    #returning the dataframe
    return describe


