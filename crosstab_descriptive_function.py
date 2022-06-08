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

