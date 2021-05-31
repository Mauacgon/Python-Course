import pandas as pd
import glob
import os
import logging

def listPatternFiles(searchDir, pattern):
    files = glob.glob(os.path.join(searchDir, pattern))
    
def comp_type(output_df_type,ref_df_type):  
    return (output_df_type.dtypes.values == input_df_type.dtypes.values).all()
    
def comp_names(output_df_col,ref_df_col):
    return (output_df_col.columns == ref_df_col.columns).all()

    
def is_equal(output_df,ref_df):
    same_dim = output_df.shape == ref_df.shape
    same_type = comp_type(output_df, ref_df)
    same_name = comp_names(output_df,ref_df)
    
    return same_dim + same_type + same_name == 3
    

def compareSingleFile(outputfile, referenceFile, delimiter = ';', decimal='.'):
    outputData = pd.read_csv(outputFile, delimiter=delimiter, decimal=decimal)
    referenceData = pd.read_csv(referenceFile, delimiter=delimiter, decimal=decimal)
    
    return is_equal(outputData, referenceData)

def compareFiles(workingDir,outputFilePattern, refFileDir, refFileName):
    equal = []
    listOutputfiles = listPatternFiles(workingDir, outputFilePattern)
    refFile = listPatternFiles(refFileDir,refFileName)
    for file in listOutputFiles:
        equal.append(compareSingleFile(file,refFile))
        
    return all(equal)
