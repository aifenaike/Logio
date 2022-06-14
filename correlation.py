from pandas import DataFrame

def correl(df : DataFrame, method : str = 'pearson'):
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
    from pandas import DataFrame

    # Coerce the input into a dataframe if it is not one already
    df = DataFrame(df) 

    # Drop NA values from the dataframe
    df.dropna(inplace = True) 
    
    # Selects the numerical columns in the dataframe
    new_df = df.select_dtypes(include = 'number') 
    
    return new_df.corr(method = method)